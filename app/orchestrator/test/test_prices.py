# -*-coding:utf8-*-
import unittest
from datetime import datetime
from typing import List

from prio.models.schemas import PriceRule, SegmentPriceInfo
from prio.services.price_service import getMatchPricesRule, getPrice, getMarkupsToSum

'''
TABLE RULES

+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
| haul | origin | destination | weekday | from      | to        | price | markup_ranges | markups   | #  |
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
| DO   |        |             |         |           |           | 7.00  |               |           | 1  | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
| MH   |        |             | V|S|D   |           |           | 10.00 |               |           | 2  | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
| MH   |        |             |         |           |           | 9.00  |               |           | 3  | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
| LH   |        |             |         |           |           | 12.00 | 50|75         | 1,50|2,50 | 4  | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
|      | MAD    | BIO         |         |           |           | 6.00  |               |           | 5  | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
|      | BIO    | MAD         |         |           |           | 6.00  |               |           | 6  | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
|      | MAD    | BIO         |         | 15/6/2021 | 15/9/2021 | 7.50  |               |           | 7  | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
|      | BIO    | MAD         |         | 15/6/2021 | 15/9/2021 | 7.50  |               |           | 8  | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
|      | MAD    | LHR         | L|J     | 15/6/2021 | 15/9/2021 | 11.00 |               |           | 9  | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
|      | LHR    | MAD         | L|J     | 15/6/2021 | 15/9/2021 | 11.00 |               |           | 10 | X
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
|      | MAD    | BUE         | L|J     |           |           | 13.00 |               |           | 11 | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
|      | BUE    | MAD         | L|J     |           |           | 13.00 |               |           | 12 | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
|      | MAD    | JFK         |         |           |           | 11.00 | 50            | 1         | 13 | x
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+
|      | JFK    | MAD         |         |           |           | 11.00 |               |           | 14 |
+------+--------+-------------+---------+-----------+-----------+-------+---------------+-----------+----+

Campos:
haul:
Habrá 3 opciones para rellenar este campo (DO, MH o LH), que marcarán el precio por defecto según el haul. No será combinable con origin+destination.
origin+destination:
Se utilizará para especificar precios por ruta. No será combinable con haul.

weekday:
Se utilizará para especificar precios distintos en ciertos días de la semana. Podrá tener múltiples valores separados por “|”: L|M|X|J|V|S|D.
Deberá ir combinado con haul o con origin+destination. Podrá combinarse con el from+to.

from+to:
Se utilizará para especificar precios distintos en un rango de fechas. Tendrá el formato DD/MM/YYYY.
Deberá ir combinado con haul o con origin+destination. Podrá combinarse con el from+to.

price:
Determina el precio del PB en EUR (ej: 7,00)
markup_ranges-markups:
Se utilizará para establecer un sobreprecio en EUR según % de PB vendidos/inventario. Podrá tener múltiples valores separados por “|”.
El primer campo (markup_ranges) determina los % a partir de los que aplicar el sobreprecio.
El segundo campo (markups) determina los sobreprecios para los rangos del campo anterior
Ejemplo: markup_ranges=40|70 y markups=1,50|2,50 => A partir de un 40% se aplica un sobreprecio de 1,50 EUR y a partir de 70% se aplica un sobreprecio de 2,50 EUR.

Resolución de conflictos:
En caso de que vayas líneas apliquen, se eligirá el precio de la más restrictiva (origin+destination > haul // from+to > weekday):
origin+destination es más restrictivo que haul (ej: el precio de un origin+destination MAD-BIO prevalece sobre el precio de un haul DO)
to-from es más restrictivo que weekday (prevalece el precio de la línea que tenga to-from), y una línea que tenga to-from y weekday combinados es más restrictiva que otra que sólo tenga una de las dos opciones
- Casos extremos
- getCorrectRule(haul='PA', origin='MAD', destination='BCN', departure_date='2020-08-14'(V) ) -> PriceRule ??
- hay que fitrar las reglas con todos los inputs nulos
'''


class TestUtils(unittest.TestCase):

    # TODO mejor mockear
    def getRules(self) -> List[PriceRule]:
        """
        Return a list with all required rules to test.
        """
        return [
            PriceRule('1', 'DO', None, None, None, None, None, '7.00', None, None),
            PriceRule('3', 'MH', None, None, None, None, None, '9.00', None, None),
            PriceRule('4', 'LH', None, None, None, None,
                      None, '12.00', '50|75', '1,50|2,50'),
            PriceRule('11', None, "MAD", "BUE", "L|J", None, None, '13.00', None, None),
            PriceRule('12', None, "BUE", "MAD", "L|J", None, None, '13.00', None, None),
            PriceRule('7', None, "MAD", "BIO", None, "15/6/2021",
                      "15/9/2021", '7.50', None, None),
            PriceRule('2', 'MH', None, None, 'V|S|D', None, None, '10.00', None, None),
            PriceRule('5', None, "MAD", "BIO", None, None, None, '6.00', None, None),
            PriceRule('6', None, "BIO", "MAD", None, None, None, '6.00', None, None),
            PriceRule('14', None, "JFK", "MAD", None, None, None, '11.0', None, None),
            PriceRule('13', None, "MAD", "JFK", None, None, None, '11.0', '50', '1'),
            PriceRule('8', None, "BIO", "MAD", None, "15/6/2021",
                      "15/9/2021", '7.50', None, None),
            PriceRule('9', None, "MAD", "LHR", "L|J", "15/6/2021",
                      "15/9/2021", '11.00', None, None),
            PriceRule('10', None, "LHR", "MAD", "L|J", "15/6/2021",
                      "15/9/2021", '11.00', None, None)
        ]

    def test_regla1_dado_un_vuelo_con_haul_DO_y_sin_coincidencia_en_el_resto_de_campos(self):
        input = SegmentPriceInfo(haul='DO', origin='MAD',
                                 destination='BCN', departure_date=datetime(2020, 8, 14))
        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '1')

        print("Regla1 - Precio: ", getPrice(rule))
        print("Regla1 - Markup: ", getMarkupsToSum(rule, "55"))

    def test_regla3_dado_un_vuelo_con_haul_MH_y_sin_coincidencia_en_el_resto_de_campos(self):
        input = SegmentPriceInfo(haul='MH', origin='MAD',
                                 destination='BCN', departure_date=datetime(2020, 8, 13))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '3')

        print("Regla3 - Precio: ", getPrice(rule))
        print("Regla3 - Markup: ", getMarkupsToSum(rule, "55"))

    def test_regla4_dado_un_vuelo_con_haul_LH_y_sin_coincidencia_en_el_resto_de_campos(self):
        input = SegmentPriceInfo(haul='LH', origin='MAD',
                                 destination='BCN', departure_date=datetime(2020, 8, 13))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '4')

        print("Regla4 - Precio: ", getPrice(rule))
        print("Regla4 - Markup: ", getMarkupsToSum(rule, "75"))

    def test_regla2_dado_un_vuelo_con_haul_MH_y_dia_de_la_semana_V(self):
        input = SegmentPriceInfo(haul='MH', origin='MAD',
                                 destination='BCN', departure_date=datetime(2020, 8, 14))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '2')

        print("Regla2 - Precio: ", getPrice(rule))
        print("Regla2 - Markup: ", getMarkupsToSum(rule, "55"))

    def test_regla5_dado_origin_y_destination_MAD_BIO_y_sin_coincidencia_en_campos_de_fecha(self):
        input = SegmentPriceInfo(haul='DO', origin='MAD',
                                 destination='BIO', departure_date=datetime(2020, 8, 14))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '5')

        print("Regla5 - Precio: ", getPrice(rule))
        print("Regla5 - Markup: ", getMarkupsToSum(rule, "55"))

    def test_regla6_dado_origin_y_destination_BIO_MAD_y_sin_coincidencia_en_campos_de_fecha(self):
        input = SegmentPriceInfo(haul='DO', origin='BIO',
                                 destination='MAD', departure_date=datetime(2020, 8, 14))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '6')

        print("Regla6 - Precio: ", getPrice(rule))
        print("Regla6 - Markup: ", getMarkupsToSum(rule, "55"))

    def test_regla14_dado_origin_y_destination_JFK_MAD_y_sin_coincidencia_en_campos_de_fecha(self):
        input = SegmentPriceInfo(haul='DO', origin='JFK',
                                 destination='MAD', departure_date=datetime(2020, 8, 14))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '14')

        print("Regla4 - Precio: ", getPrice(rule))
        print("Regla4 - Markup: ", getMarkupsToSum(rule, "55"))

    def test_regla13_dado_origin_y_destination_MAD_JFK_y_sin_coincidencia_en_campos_de_fecha(self):
        input = SegmentPriceInfo(haul='LH', origin='MAD',
                                 destination='JFK', departure_date=datetime(2020, 8, 14))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '13')

        print("Regla13 - Precio: ", getPrice(rule))
        print("Regla13 - Markup: ", getMarkupsToSum(rule, "100"))

    def test_regla11_dado_origin_y_destinatio_MAD_BUE_y_dia_de_la_semana_L(self):
        input = SegmentPriceInfo(haul='DO', origin='MAD',
                                 destination='BUE', departure_date=datetime(2020, 8, 17))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '11')

        print("Regla11 - Precio: ", getPrice(rule))
        print("Regla11 - Markup: ", getMarkupsToSum(rule, "55"))

    def test_regla12_dado_origin_y_destinatio_BUE_MAD_y_dia_de_la_semana_L(self):
        input = SegmentPriceInfo(haul='DO', origin='BUE',
                                 destination='MAD', departure_date=datetime(2020, 8, 17))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '12')

        print("Regla12 - Precio: ", getPrice(rule))
        print("Regla12 - Markup: ", getMarkupsToSum(rule, "55"))

    def test_regla7_dado_origin_y_destinatio_MAD_BIO_con_coincidencia_en_campo_de_fecha_y_SIN_dia_de_la_semana(self):
        input = SegmentPriceInfo(haul='DO', origin='MAD',
                                 destination='BIO', departure_date=datetime(2021, 8, 24))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '7')

        print("Regla7 - Precio: ", getPrice(rule))
        print("Regla7 - Markup: ", getMarkupsToSum(rule, "55"))

    def test_regla8_dado_origin_y_destinatio_BIO_MAD_con_coincidencia_en_campo_de_fecha_y_SIN_dia_de_la_semana(self):
        input = SegmentPriceInfo(haul='DO', origin='BIO',
                                 destination='MAD', departure_date=datetime(2021, 8, 24))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '8')

        print("Regla8 - Precio: ", getPrice(rule))
        print("Regla8 - Markup: ", getMarkupsToSum(rule, "55"))

    def test_regla9_dado_origin_y_destinatio_MAD_LHR_con_coincidencia_en_campo_de_fecha_y_dia_de_la_semana_L(self):
        input = SegmentPriceInfo(haul='DO', origin='MAD',
                                 destination='LHR', departure_date=datetime(2021, 8, 23))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '9')

        print("Regla9 - Precio: ", getPrice(rule))
        print("Regla9 - Markup: ", getMarkupsToSum(rule, "55"))

    def test_regla10_dado_origin_y_destinatio_LHR_MAD_con_coincidencia_en_campo_de_fecha_y_dia_de_la_semana_L(self):
        input = SegmentPriceInfo(haul='DO', origin='LHR',
                                 destination='MAD', departure_date=datetime(2021, 8, 23))

        rule = getMatchPricesRule(input, self.getRules())

        self.assertEqual(rule.id, '10')

        print("Regla10 - Precio: ", getPrice(rule))
        print("Regla10 - Markup: ", getMarkupsToSum(rule, "55"))


if __name__ == '__main__':
    unittest.main()
