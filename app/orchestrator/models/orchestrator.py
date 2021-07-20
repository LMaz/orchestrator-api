from pydantic import BaseModel, Field
from typing import List, Optional, Union


class Message(BaseModel):
    message: str


class InfantCoupon(BaseModel):
    id: str = Field(None, title="ID",
                    description="ID", example="INFANT_01")
    coupon: str = Field(None, title="Coupon",
                        description="Coupon", example="INF")
    farebasis: str = Field(None, title="Farebasis",
                           description="Farebasis", example="XDFF")
    numberTicket: str = Field(None, title="Ticket Number",
                              description="Ticket Number", example="075000000003")
    ticketDesignator: str = Field(None, title="Ticket Designator",
                                  description="Ticket Designator")
    issueDate: str = Field(None, title="Issue Date",
                           description="Issue Date", example="2019-02-25")


class FranchisePiece(BaseModel):
    subtype: str = Field(None, title="Subtype",
                         description="Subtype", example="BAGGAGE_23")
    units: int = Field(None, title="Units",
                       description="Units", example=2)
    description: str = Field(None, title="Description",
                             description="Description", example="23Kg")


class Seat(BaseModel):
    row: str = Field(None, title="Row",
                     description="Row", example="12")
    column: str = Field(None, title="Column",
                        description="Column", example="A")


class Status(BaseModel):
    message: str = Field(None, title="Message",
                         description="Message", example="CHECKABLE")
    code: str = Field(None, title="Code",
                      description="Code", example="CHECKABLE")


class ExtraPiece(BaseModel):
    subtype: str = Field(None, title="Subtype", example="BAGGAGE_23")
    units: int = Field(None, title="Units", example=2)
    description: str = Field(None, title="Description", example="23Kg")
    reasons: List[str] = Field(None, title="Reasons", example="TOP TIER")


class FrequentFlyer(BaseModel):
    number: str = Field(None, title="Frequent Flyer Number",
                        description="Frequent Flyer Number", example="72749559")
    level: str = Field(None, title="FF Level",
                       description="FF Level", example="8")
    topTier: str = Field(None, title="Top Tier",
                         description="Top Tier", example="CLA")
    company: str = Field(None, title="Company",
                         description="Company", example="IB")


class CabinClass(BaseModel):
    type: str = Field(None, title="Cabin Type",
                      description="Cabin Type", example="ECONOMY")
    rbd: str = Field(None, title="RBD",
                     description="RBD", example="0")


class Cabin(BaseModel):
    cabinClass: CabinClass = Field(None, title="Cabin Class")
    carrier: str = Field(..., title="Carrier",
                         description="Carrier", example="IB")


class Flight(BaseModel):
    cabin: Cabin = Field(..., title="Cabin")
    flightNumber: str = Field(..., title="Flight Number",
                              description="Flight Number", example="3482")


class PassengerCoupon(BaseModel):
    infantCoupon: InfantCoupon = Field(None, title="InfantCoupon")
    coupon: str = Field(None, title="Coupon",
                        description="Coupon", example="1")
    farebasis: str = Field(None, title="Farebasis",
                           description="Farebasis", example="ODNNANB5")
    franchisePieces: List[FranchisePiece] = Field(None, title="Franchise Pieces")
    numberTicket: str = Field(None, title="Ticket Number",
                              description="Ticket Number", example="0752391826332")
    ticketDesignator: str = Field(None, title="Ticket Designator",
                                  description="Ticket Designator")
    seat: Seat = Field(None, title="Seat")
    extraPieces: List[ExtraPiece] = Field(None, title="Extra Pieces")
    eligible: bool = Field(None, title="Eligible",
                           description="Eligible", example=True)
    issueDate: str = Field(None, title="Issue Date",
                           description="Issue Date", example="2020-07-08T22:00:00.000Z")
    id: str = Field(None, title="ID",
                    description="ID", example="ADULT_01")
    status: Status = Field(None, title="Status")


class Slice(BaseModel):
    segmentIds: List[str] = Field(None, title="Segment IDs")
    id: str = Field(None, title="Slice ID",
                    description="Slice ID", example="GVAMAD20200807191500")


class TicketPrice(BaseModel):
    currency: str = Field(None, title="Currency",
                          description="Currency", example="CHF")
    number: str = Field(None, title="Number",
                        description="Number", example="0752391826332")
    tax: int = Field(None, title="Tax",
                     description="Tax", example=47.15)
    fare: int = Field(None, title="Fare",
                      description="Fare", example=43)
    total: int = Field(None, title="Total",
                       description="Total", example=90.15)


class Infant(BaseModel):
    id: str = Field(None, title="ID",
                    description="ID", example="INFANT_01")
    surname: str = Field(None, title="Surname",
                         description="Surname", example="PRUEBAS")
    name: str = Field(None, title="Name",
                      description="Name", example="BEBE")
    ticketPrices: List[TicketPrice] = Field(..., title="Ticket Prices", min_items=1)
    birthDate: str = Field(None, title="ID",
                           description="ID", example="2018-12-30")


class Segment(BaseModel):
    operatingFlight: Flight = Field(..., title="Operating Flight")
    arrivalDate: str = Field(None, title="Arrival Date",
                             description="Arrival Date", example="2020-08-07 21:20")
    utcArrivalDate: str = Field(None, title="UTC Arrival Date",
                                description="UTC Arrival Date", example="2020-08-07 19:20")
    marketingFlight: Flight = Field(None, title="Marketing Flight")
    flown: bool = Field(None, title="Flown?",
                        description="Flown?", example=False)
    arrivalAirport: str = Field(..., title="Arrival Airport",
                                description="Arrival Airport", example="MAD")
    departureAirport: str = Field(..., title="Departure Airport",
                                  description="Departure Airport", example="GVA")
    departureDate: str = Field(..., title="Departure Date",
                               description="Departure Date", example="2020-08-07 19:15")
    edifact: bool = Field(None, title="EDIFACT?",
                          description="EDIFACT?", example=False)
    passengerCoupons: List[PassengerCoupon] = []
    pricesProvider: str = Field(None, title="Prices Provider",
                                description="Prices Provider", example="TARIFICATOR")
    utcDepartureDate: str = Field(None, title="UTC Departure Date",
                                  description="UTC Departure Date", example="2020-08-07 17:15")
    time: str = Field(None, title="Time",
                      description="Time", example="BKI")
    id: str = Field(None, title="ID",
                    description="ID", example="IB349320200807")


class Passenger(BaseModel):
    surname: str = Field(None, title="Surname",
                         description="Surname", example="IOAS")
    frequentFlyer: FrequentFlyer = Field(None, title="FrequentFlyer")
    name: str = Field(None, title="Name",
                      description="Name", example="CHARLES")
    passengerType: str = Field(None, title="Passenger Type",
                               description="Passenger Type", example="ADULT")
    ticketPrices: List[TicketPrice] = Field(..., title="Ticket Prices", min_items=1)
    items: List[str] = Field(None, title="items")
    title: str = Field(None, title="Title",
                       description="Title", example="MR")
    infant: Infant = Field(None, title="Infant")
    resiberId: str = Field(None, title="Resiber ID",
                           description="Resiber ID", example="2")
    birthDate: str = Field(None, title="Birth Date",
                           description="Birth Date", example="1980-01-02")
    id: str = Field(None, title="ID",
                    description="ID", example="ADULT_01")


class Context(BaseModel):
    issueOffice: str = Field(None, title="Issue Office",
                             description="Issue Office", example="ZRH175")
    locator: str = Field(None, title="Locator",
                         description="Locator", example="RHFJIT")
    checkinFlowMode: str = Field(None, title="Checkin Flow Mode",
                                 description="Checkin Flow Mode", example="REGULAR")
    slices: List[Slice] = Field(None, title="Slices")
    issueCountry: str = Field(None, title="Issue Country",
                              description="Issue Country", example="CH")
    bookingDate: str = Field(None, title="Booking Date",
                             description="Booking Date", example="2020-08-04 15:53")
    segments: List[Segment] = Field(..., title="Segments", min_items=1)
    flownSegments: bool = Field(None, title="Flown Segments?",
                                description="Flown Segments?", example=False)
    paymentMode: str = Field(None, title="Payment Mode",
                             description="Payment Mode", example="ONLINE")
    passengers: List[Passenger] = Field(..., title="Passengers", min_items=1)
    issueCurrency: str = Field(None, title="Issue Currency",
                               description="Issue Currency", example="CHF")
    dynamicPricing: bool = Field(None, title="Dynamic Pricing?", description="Dynamic Pricing?", example=False)


class PurchasedBaggage(BaseModel):
    code: str = Field(..., title="code",
                         description="code", example="0LM")
    units: int = Field(None, title="units",
                       description="Units", example="2")


class Type(BaseModel):
    pieces: str = Field(..., title="pieces",
                              description="pieces", example="2")
    code: str = Field(..., title="code",
                         description="code", example="0LM")


class PaxId(BaseModel):
    id: str = Field(..., title="Ancillary segmentIds",
                    description="Ancillary segmentIds", example="ADULT_01")
    purchased: List[PurchasedBaggage] = Field(..., title="purchasedBaggage")

    types: List[Type] = Field(..., title="purchasedBaggage")


class Slices(BaseModel):
    id: str = Field(..., title="Ancillary segmentIds",
                    description="Ancillary segmentIds", example="IB349320200807")
    passengers: List[PaxId] = Field(..., title="passengers")


class SegmentIds(BaseModel):
    id: str = Field(..., title="Ancillary segmentIds",
                    description="Ancillary segmentIds", example="IB349320200807")
    passengers: List[str] = Field(..., title="passengers")


class Request(BaseModel):
    currency: str = Field(..., title="Currency",
                          description="Currency", example="EUR")
    type: str = Field(None, title="Ancillary type",
                      description="Ancillary type", example="PRIORITY_BOARDING")
    segmentIds: List[SegmentIds] = Field(..., title="SegmentIds", min_items=1)


class RequestBaggage(BaseModel):
    realm: str = Field(..., title="realm",
                          description="realm", example="Checkin")
    currency: str = Field(..., title="Currency",
                          description="Currency", example="EUR")
    dynamicPrices: bool = Field(..., title="dynamicPrices",
                      description="dynamicPrices", example="true")
    type: str = Field(None, title="Ancillary type",
                      description="Ancillary type", example="PRIORITY_BOARDING")

    slices: List[Slices] = Field(..., title="Slices", min_items=1)


class OrchestratorRequest(BaseModel):
    context: Context = Field(..., title="Context")
    request: Union[Request, RequestBaggage] = Field(..., title="Request")


class PassengerPrice(BaseModel):
    id: str = Field(None, title="ID",
                    description="ID", example="ADULT_01")
    amount: str = Field(None, title="Amount",
                        description="Amount", example='40.18')


class ResponseStatus(BaseModel):
    reason: str = Field(None, title="Reason",
                        description="Reason", example="prices not charged")
    code: str = Field(None, title="Code",
                      description="Code", example="NOT_AVAILABLE", alias="code")


class PricesResponse(BaseModel):
    _from: int = Field(..., title="from",
                    description="from", example="1", alias='from')
    to: int = Field(..., title="to",
                    description="to", example="1")
    amount: float = Field(..., title="amount",
                    description="amount", example="20.1")


class TypeResponse(BaseModel):
    prices: List[PricesResponse] = Field(..., title="price",
                    description="price")

    code: str = Field(..., title="code")


class PaxIdResponse(BaseModel):
    id: str = Field(..., title="Ancillary segmentIds",
                    description="Ancillary segmentIds", example="ADULT_01")

    types: List[TypeResponse] = Field(..., title="typeResponse")


class SlicesResponse(BaseModel):
    id: str = Field(..., title="Ancillary segmentIds",
                    description="Ancillary segmentIds", example="IB349320200807")
    passengers: List[PaxIdResponse] = Field(..., title="passengers")


class OrchestratorResponse(BaseModel):
    currency: str = Field(..., title="Currency",
                          description="Currency", example="EUR")
    dynamicPrices: bool = Field(..., title="dynamicPrices",
                                description="dynamicPrices", example="true")
    type: str = Field(None, title="Ancillary type",
                      description="Ancillary type", example="BAGGAGE")

    slices: List[SlicesResponse] = Field(..., title="Slices", min_items=1)
