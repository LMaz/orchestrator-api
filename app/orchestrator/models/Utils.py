from pydantic import BaseModel, Field


class ResponseStatus(BaseModel):  # TODO: repetido! Mover a un archivo comun
    code: str = Field(..., example='OK', regex=r'(OK)|(KO)')
    reason: str = Field(None)