# -*-coding:utf8-*-
import os

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from app.orchestrator.models.orchestrator import Message, OrchestratorResponse, OrchestratorRequest
from app.orchestrator.models.calendar import CalendarRequest
from app.orchestrator.services.dynamoDB import getItem

# from lucas.security import get_api_key

router = APIRouter()

X_API_KEY = APIKeyHeader(name='x-api-key')


def get_api_key(x_api_key: str = Depends(X_API_KEY)):
    """ validates the x-api-key and raises a 401 if invalid """
    if x_api_key == os.environ['X_API_KEY']:
        return
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )


@router.get("/health",
            summary='Health check.',
            tags=["HEALTH"]
            )
def health():
    return {"UP"}
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

def requestRules(url: str, payload: dict, x_api_key: str) -> dict:
    response = requests.post(
        url,
        headers={
            "x-api-key": x_api_key,
            "content-type": "application/json",
        },
        verify=False,
        json=payload,
    )

    return response.json()


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
callback_url = "http://127.0.0.1:8008/ODM_API"
calendar_callback_router = APIRouter()


@calendar_callback_router.post("{$callback_url}", response_model=OrchestratorResponse)
def invoice_notification(body: CalendarRequest):
    body
    pass


@router.post('/', callbacks=calendar_callback_router.routes, response_model=OrchestratorResponse,
             description="Petición para orquestrar las peticiones y redirigir al servicio adecuado")
def orchestrator(orchestrator_request: OrchestratorRequest):
    """
    Retrieve flight offer recommendation for a given passenger id
    """

    context, request = orchestrator_request.context, orchestrator_request.request

    if request.dynamicPrices:

        response = requestRules(
            "http://127.0.0.1:8008/ODM_API",
            request,
            '1234567890'
        )

        # table = os.environ['DYNAMODB_KNOWN_CLIENTS']
        # getItem(table, {"key": "a"})
    else:
        response = {'fuck': 'my life'}
    return response
