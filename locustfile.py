import json
import os

from locust import HttpUser, between, task

lock_request = {
    "locator": "KLDSD",
    "arrivalAirport": "MAD",
    "departureAirport": "GVA",
    "departureDate": "2020-08-07",
    "carrier": "IB",
    "flightNumber": "3493",
    "quantity": 2
}

unlock_request = {
    "locator": "KLDSD",
    "arrivalAirport": "MAD",
    "departureAirport": "GVA",
    "departureDate": "2020-08-07",
    "carrier": "IB",
    "flightNumber": "3493",
                    "quantity": 2
}

confirm_request = {
    "locator": "KLDSD",
    "arrivalAirport": "MAD",
    "departureAirport": "GVA",
    "departureDate": "2020-08-07",
    "carrier": "IB",
    "flightNumber": "3493",
                    "quantity": 2
}

price_request = {
    "context": {
        "issueOffice": "ZRH175",
        "locator": "RHFJIT",
        "checkinFlowMode": "REGULAR",
        "slices": [
            {
                "segmentIds": [
                    "IB349320200807"
                ],
                "id": "GVAMAD20200807191500"
            },
            {
                "segmentIds": [
                    "IB348220200828"
                ],
                "id": "MADGVA20200828203000"
            }
        ],
        "issueCountry": "CH",
        "bookingDate": "2020-08-04 15:53",
        "segments": [
                        {
                            "operatingFlight": {
                                "cabin": {
                                    "cabinClass": {
                                        "type": "ECONOMY",
                                        "rbd": "O"
                                    },
                                    "carrier": "IB"
                                },
                                "flightNumber": "3493"
                            },
                            "arrivalDate": "2020-08-07 21:20",
                            "utcArrivalDate": "2020-08-07 19:20",
                            "marketingFlight": {
                                "cabin": {
                                    "cabinClass": {
                                        "type": "ECONOMY",
                                        "rbd": "O"
                                    },
                                    "carrier": "I2"
                                },
                                "flightNumber": "3493"
                            },
                            "flown": False,
                            "arrivalAirport": "MAD",
                            "departureAirport": "GVA",
                            "departureDate": "2020-08-07 19:15",
                            "edifact": False,
                            "passengerCoupons": [
                                {
                                    "infantCoupon": {
                                        "id": "INFANT_01",
                                        "coupon": "INF",
                                        "farebasis": "XDFF",
                                        "numberTicket": "075000000003",
                                        "ticketDesignator": None,
                                        "issueDate": "2019-02-25"
                                    },
                                    "coupon": "1",
                                    "farebasis": "ODNNANB5",
                                    "franchisePieces": [
                                        {
                                            "subtype": "BAGGAGE_23",
                                            "units": 2,
                                            "description": "23Kg"
                                        }
                                    ],
                                    "numberTicket": "0752391826332",
                                    "ticketDesignator": None,
                                    "seat": {
                                        "row": "12",
                                        "column": "A"
                                    },
                                    "extraPieces": [],
                                    "eligible": True,
                                    "issueDate": "2020-07-08T22:00:00.000Z",
                                    "id": "ADULT_01",
                                    "status": {
                                        "message": "CHECKABLE",
                                        "code": "CHECKABLE"
                                    }
                                },
                                {
                                    "infantCoupon": None,
                                    "coupon": None,
                                    "farebasis": "ODNNANB5",
                                    "franchisePieces": [],
                                    "numberTicket": None,
                                    "ticketDesignator": None,
                                    "seat": {
                                        "row": "12",
                                        "column": "A"
                                    },
                                    "extraPieces": [],
                                    "eligible": True,
                                    "issueDate": None,
                                    "id": "ADULT_02",
                                    "status": {
                                        "message": "CHECKABLE",
                                        "code": "CHECKABLE"
                                    }
                                }
                            ],
                            "pricesProvider": "TARIFICATOR",
                            "utcDepartureDate": "2020-08-07 17:15",
                            "time": "BKI",
                            "id": "IB349320200807"
                        },
            {
                            "operatingFlight": {
                                "cabin": {
                                    "cabinClass": {
                                        "type": "ECONOMY",
                                        "rbd": "O"
                                    },
                                    "carrier": "IB"
                                },
                                "flightNumber": "3482"
                            },
                            "arrivalDate": "2020-08-28 22:25",
                            "utcArrivalDate": "2020-08-28 20:25",
                            "marketingFlight": None,
                            "flown": False,
                            "arrivalAirport": "GVA",
                            "departureAirport": "MAD",
                            "departureDate": "2020-08-28 20:30",
                            "edifact": False,
                            "passengerCoupons": [
                                {
                                    "infantCoupon": {
                                        "id": "INFANT_01",
                                        "coupon": "INF",
                                        "farebasis": "XDFF",
                                        "numberTicket": "075000000003",
                                        "ticketDesignator": None,
                                        "issueDate": "2019-02-25"
                                    },
                                    "coupon": None,
                                    "farebasis": "ODNNANB5",
                                    "franchisePieces": [],
                                    "numberTicket": None,
                                    "ticketDesignator": None,
                                    "seat": None,
                                    "extraPieces": [],
                                    "eligible": True,
                                    "issueDate": None,
                                    "id": "ADULT_01",
                                    "status": {
                                        "message": "CHECKABLE",
                                        "code": "CHECKABLE"
                                    }
                                },
                                {
                                    "infantCoupon": None,
                                    "coupon": None,
                                    "farebasis": "ODNNANB5",
                                    "franchisePieces": [],
                                    "numberTicket": None,
                                    "ticketDesignator": None,
                                    "seat": None,
                                    "extraPieces": [],
                                    "eligible": True,
                                    "issueDate": None,
                                    "id": "ADULT_02",
                                    "status": {
                                        "message": "CHECKABLE",
                                        "code": "CHECKABLE"
                                    }
                                }
                            ],
                            "pricesProvider": "TARIFICATOR",
                            "utcDepartureDate": "2020-08-28 18:30",
                            "time": "BKI",
                            "id": "IB348220200828"
                        }
        ],
        "flownSegments": False,
        "paymentMode": "ONLINE",
        "passengers": [
            {
                "surname": "IOAS",
                "frequentFlyer": {
                    "number": "72749559",
                    "level": "8",
                    "topTier": "CLA",
                    "company": "IB"
                },
                "name": "CHARLES",
                "passengerType": "ADULT",
                "ticketPrices": [
                    {
                        "currency": "CHF",
                                    "number": "0752391826332",
                                    "tax": 47.15,
                                    "fare": 43,
                                    "total": 90.15
                    }
                ],
                "items": [
                    "DEAF"
                ],
                "title": "MR",
                "infant": {
                    "id": "INFANT_01",
                    "surname": "PRUEBAS",
                    "name": "BEBE",
                    "ticketPrices": [
                        {
                            "currency": "EUR",
                                        "number": "075000000003",
                                        "tax": 32.91,
                                        "fare": 25,
                                        "total": 62.91
                        }
                    ],
                    "birthDate": "2018-12-30"
                },
                "resiberId": "2",
                "birthDate": "1980-01-02",
                "id": "ADULT_01"
            },
            {
                "surname": "GARCIAMONTOYA",
                "frequentFlyer": None,
                "name": "ERIKAPATRICIA",
                "passengerType": "ADULT",
                "ticketPrices": [
                    {
                        "currency": "CHF",
                                    "number": "",
                                    "tax": 47.15,
                                    "fare": 43,
                                    "total": 90.15
                    }
                ],
                "items": [],
                "title": None,
                "infant": None,
                "resiberId": "1",
                "birthDate": None,
                "id": "ADULT_02"
            }
        ],
        "issueCurrency": "CHF",
        "dynamicPricing": False
    },
    "request": {
        "currency": "EUR",
        "type": "PRIORITY_BOARDING",
                    "segmentIds": [
                        {
                            "id": "IB349320200807",
                            "passengers": [
                                "ADULT_01"
                            ]
                        },
                        {
                            "id": "IB034020200808",
                            "passengers": [
                                "ADULT_01"
                            ]
                        }
                    ]
    }
}


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def health(self):
        self.client.get("/health")

    @task
    def _lock(self):
        self.client.post("/_lock/0001", headers={"accept": "application/json", "x-api-key": os.environ['X_API_KEY'], "Content-Type": "application/json"},
                         data=json.dumps(lock_request))

    @task
    def _unlock(self):
        self.client.post("/_unlock/0001", headers={"accept": "application/json", "x-api-key": os.environ['X_API_KEY'], "Content-Type": "application/json"},
                         data=json.dumps(unlock_request))

    @task
    def request_priority_confirm(self):
        self.client.post("/request_priority_confirm/0001", headers={"accept": "application/json", "x-api-key": os.environ['X_API_KEY'], "Content-Type": "application/json"},
                         data=json.dumps(confirm_request))

    @task
    def request_priority_boarding(self):
        self.client.post("/request_priority_boarding", headers={"accept": "application/json", "x-api-key": os.environ['X_API_KEY'], "Content-Type": "application/json"},
                         data=json.dumps(price_request))
