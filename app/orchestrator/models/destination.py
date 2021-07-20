# -*-coding:utf8-*-
from typing import List

from pydantic import BaseModel, Field, validator
from app.orchestrator.models.Utils import ResponseStatus


class TripRecommendation(BaseModel):
    origin: str = Field(None, description='Outbound origin', regex=r'^[A-Z]{3}$', example='MAD')
    destination: str = Field(..., description='Outbound destination', regex=r'^[A-Z]{3}$', example='AMS')
    recommendationSource: str = Field(..., description='The data source for the recommendation')


class OfferPriceFeed(BaseModel):
    origin: str = Field(..., description='Outbound origin', regex=r'^[A-Z]{3}$', example='MAD')
    destination: str = Field(..., description='Outbound destination', regex=r'^[A-Z]{3}$', example='AMS')
    amount: float = Field(..., description='Roundtrip price', ge=0, example=350.75)
    currency: str = Field(..., regex=r'^[A-Z]{3}$', example='EUR')
    priceSource: str = Field(None, description='The price source')
    outbound_inbound_dates: List[str] = Field(
        ...,
        description='Lists of outbound-inbound date pairs. Sorted',
        min_items=1,
        example=['2021-01-01,2021-01-01', '2021-01-01,2021-01-02']
    )


class DestinationRequest(BaseModel):
    clientid: str = Field(..., description="GA's visitor id (cookie)", example="49196778618165747672")
    continent: str = Field(None, description="The client's current continent", example='Europe')
    country: str = Field(None, description="The client's current country", example='Spain')
    region: str = Field(None, description="The client's current region within the country", example='Madrid')
    market: str = Field(..., description="IBCOM's market (or point of sale)", regex=r'^[A-Z]{2}$', example='ES')
    currency: str = Field(None, description='Currency', regex=r'^[A-Z]{3}$', example='EUR')


# ----------------------------------------------
class Destination(BaseModel):
    origin: str = Field(..., description='Outbound origin city code', regex=r'^[A-Z]{3}$', example='MAD')
    destination: str = Field(..., description='Outbound destination city code', regex=r'^[A-Z]{3}$', example='AMS')
    outboundDate: str = Field(None, description='Outbound date', example='2021-01-01')
    inboundDate: str = Field(None, description='Inbound date', example='2021-03-01')
    amount: float = Field(None, description='Total amount (or ticket price)', ge=0, example=350.75)
    currency: str = Field(None, description='Currency', regex=r'^[A-Z]{3}$', example='EUR')
    priceSource: str = Field(None, description='The data source for the price. Deprecated.')
    recommendationSource: str = Field(None, description='The data source for the recommendation')

    @validator('inboundDate')  # NOTE: validator on latest defined value.
    def bothInboundAndOutboundDatesMustCoexistOrNotExist(cls, v, values, **kwargs):
        mutually_inclusive_fields = (values.get('outboundDate'), v)
        if any(mutually_inclusive_fields) and not all(mutually_inclusive_fields):
            raise ValueError('Both dates must exist. Or both must not exist.')
        return v

    @validator('inboundDate')
    def outboundDateBeforeInboundDate(cls, v, values):
        if v is not None:
            if v < values.get('outboundDate'):
                raise ValueError('OutboundDate must be same-day or earlier than InboundDate')
        return v


class DestinationResponse(BaseModel):
    destination: Destination = Field(None, description='Destination instance')
    status: ResponseStatus = Field(..., description='ResponseStatus instance')

