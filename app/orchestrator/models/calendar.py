from typing import List

from pydantic import BaseModel, Field
from app.orchestrator.models.Utils import ResponseStatus


class Offer(BaseModel):
    departureDate: str = Field(
        ...,
        description='Flight return date',
        regex=r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
        alias='outbounddate')  # Este regex es aprox.
    returnDate: str = Field(
        None,
        description='Flight return date. None when roundtrip is False',
        regex=r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
        alias='inbounddate')
    price: float = Field(
        ...,
        description='Flight total price',
        ge=0,
        alias='amount')
    ttl: int = Field(None, description='Expiration timestamp')
    unixTimestamp: int = Field(None, description='Uploaded timestamp', alias='unix_timestamp')
    realPrice: bool = Field(None, description='If price estimated from oneway offers', alias='iscalculatedprice')


class CalendarRequest(BaseModel):
    origin: str = Field(..., description='Origin city code', regex=r'^[A-Z]{3}$')
    destination: str = Field(..., description='Destination city code', regex=r'^[A-Z]{3}$')
    currency: str = Field(..., description='Currency', regex=r'^[A-Z]{3}$')
    market: str = Field(..., description="IBCOM's market (or point of sale)", regex=r'^[A-Z]{2}$')
    roundtrip: bool = Field(..., description='True if roundtrip flight, else False')


class Calendar(CalendarRequest):
    offers: List[Offer] = Field(..., description='List of offer instances')


class CalendarResponse(BaseModel):
    calendar: Calendar = Field(None, description='Calendar instance')
    status: ResponseStatus = Field(..., description='ResponseStatus instance')
