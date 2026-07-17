"""Esquemas Pydantic: validan y documentan el cuerpo de las peticiones de la API."""

from pydantic import BaseModel, Field


class VerificarDniRequest(BaseModel):
    """Cuerpo de POST /api/auth/verificar."""
    dni: str = Field(..., min_length=8, max_length=8)
    fecha_nacimiento: str = Field(..., description="Formato AAAA-MM-DD")


class VotoRequest(BaseModel):
    """Cuerpo de POST /api/votos."""
    dni: str = Field(..., min_length=8, max_length=8)
    fecha_nacimiento: str = Field(..., description="Formato AAAA-MM-DD")
    id_candidato: int
