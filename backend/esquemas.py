from pydantic import BaseModel, Field


class VerificarDniRequest(BaseModel):
    dni: str = Field(..., min_length=8, max_length=8)


class VotoRequest(BaseModel):
    dni: str = Field(..., min_length=8, max_length=8)
    id_candidato: int
