# -*-coding:utf8-*-
import unittest
from datetime import datetime
from typing import List
from prio.models.schemas import InventoryRule, SegmentInventoryInfo
from prio.services.inventory_service import getMatchInventoryRule


class TestUtils(unittest.TestCase):

    # TODO mejor mockear
    def getRules(self) -> List[InventoryRule]:
        """
        #rule | aircraft | origin | destination | flight | weekday | from | to | inventory
        No están ordenadas por prioridad. Son un ejemplo de reglas dadas por ellos.
        """
        # return [
        #        InventoryRule("1", "320",  None,  None,      None,  None,                None,                None,  8),
        #        InventoryRule("2", "320", "MAD",  None,      None,  None,                None,                None, 10),
        #        InventoryRule("3", "320", "MAD", "BIO",      None,  None,                None,                None,  7),
        #        InventoryRule("4", "320",  None,  None, "IB 2020",  None,                None,                None,  9),
        #        InventoryRule("5",  None, "MAD",  None,      None,  None,                None,                None, 12),
        #        InventoryRule("6",  None, "MAD", "BIO",      None,  None,                None,                None,  8),
        #        InventoryRule("7",  None,  None,  None, "IB 2020",  None,                None,                None, 10),
        #        InventoryRule("8",  None, "MAD",  None,      None,   "M",                None,                None,  9),
        #        InventoryRule("8",  None, "MAD",  None,      None,   "J",                None,                None,  9),
        #        ]
        return [
            InventoryRule("1", "320", None, None, None, None, None, None, 8),
            InventoryRule("2", "320", "MAD", None, None, None, None, None, 10),
            InventoryRule("3", "320", "MAD", "BIO", None, None, None, None, 7),
            InventoryRule("4", "320", None, None, "IB 2020", None, None, None, 9),
            InventoryRule("5", None, "MAD", None, None, None, None, None, 12),
            InventoryRule("6", None, "MAD", "BIO", None, None, None, None, 8),
            InventoryRule("7", None, None, None, "IB 2020", None, None, None, 10),
            InventoryRule("8", None, "MAD", None, None, "M", None, None, 9),
            InventoryRule("8", None, "MAD", None, None, "J", None, None, 9),
            InventoryRule("9", "321", "MAD", "BIO", None,
                          None, "15/6/2021", "15/9/2021", 8),
            InventoryRule("10", None, None, None, "IB 2019",
                          "M", "15/6/2021", "15/9/2021", 13),
            InventoryRule("10", None, None, None, "IB 2019",
                          "J", "15/6/2021", "15/9/2021", 13),
        ]

    def test_regla1_dado_aircraft_320(self):
        segment = SegmentInventoryInfo(
            "320", "BIO", "BCN", "IB 2345", datetime(2021, 6, 8))

        rule = getMatchInventoryRule(segment, self.getRules())

        self.assertEqual(rule.id, '1')

    def test_sin_coincidencia_en_campos(self):
        segment = SegmentInventoryInfo(
            "321", "BIO", "BCN", "IB 2347", datetime(2021, 6, 8))

        rule = getMatchInventoryRule(segment, self.getRules())

        self.assertEqual(rule, None)

    def test_regla4_dado_aircraft_320_y_flight_IB_2020(self):
        segment = SegmentInventoryInfo(
            "320", "MAD", "BCN", "IB 2020", datetime(2021, 6, 9))

        rule = getMatchInventoryRule(segment, self.getRules())

        self.assertEqual(rule.id, '4')

    def test_regla2_dado_un_aircraft_320_y_origin_MAD(self):
        segment = SegmentInventoryInfo(
            "320", "MAD", "BCN", "IB 2021", datetime(2021, 6, 10))

        rule = getMatchInventoryRule(segment, self.getRules())

        self.assertEqual(rule.id, '2')

    def test_regla4_dado_aircraft320_y_flight_IB_2020_v2(self):
        segment = SegmentInventoryInfo(
            "320", "MAD", "BIO", "IB 2020", datetime(2021, 6, 11))

        rule = getMatchInventoryRule(segment, self.getRules())

        self.assertEqual(rule.id, '4')

    # TODO: creo que esta mal. Regla 2 pide aircraft 320. Deberia ser la 5
    def test_regla2_dado_origin_MAD(self):
        segment = SegmentInventoryInfo(
            "34A", "MAD", "BCN", "IB 2018", datetime(2021, 6, 12))

        rule = getMatchInventoryRule(segment, self.getRules())

        # self.assertEqual(rule.id, '2') #ESTA MAL: deberia ser la 5!!
        self.assertEqual(rule.id, '5')

    def test_regla6_dado_origin_MAD_destination_BIO(self):
        segment = SegmentInventoryInfo(
            "34A", "MAD", "BIO", "IB 2019", datetime(2021, 6, 13))

        rule = getMatchInventoryRule(segment, self.getRules())

        self.assertEqual(rule.id, '6')

    def test_regla7_dado_flight_IB_2020(self):
        segment = SegmentInventoryInfo(
            "34A", "MAD", "BIO", "IB 2020", datetime(2021, 6, 14))

        rule = getMatchInventoryRule(segment, self.getRules())

        self.assertEqual(rule.id, '7')

    # TODO: Error, solo encuentra la 5. Comprobar.
    def test_regla8_dado_origin_y_weekday_M_o_J(self):
        segment = SegmentInventoryInfo(
            "321", "MAD", "BCN", "IB 2018", datetime(2021, 6, 15))

        rule = getMatchInventoryRule(segment, self.getRules())

        self.assertEqual(rule.id, '8')

    def test_regla5_dado_origin_MAD(self):
        segment = SegmentInventoryInfo(
            "321", "MAD", "BCN", "IB 2018", datetime(2021, 6, 16))

        rule = getMatchInventoryRule(segment, self.getRules())

        self.assertEqual(rule.id, '5')

    def test_regla10_dado_flight_IB_2109(self):
        segment = SegmentInventoryInfo(
            "321", "MAD", "BIO", "IB 2019", datetime(2021, 6, 17))

        rule = getMatchInventoryRule(segment, self.getRules())

        self.assertEqual(rule.id, '10')


if __name__ == '__main__':
    unittest.main()
