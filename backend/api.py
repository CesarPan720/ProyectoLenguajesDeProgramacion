"""API REST (FastAPI): expone SistemaElectoral/ServicioAutenticacion/analitica por HTTP
para que el frontend web pueda votar sin pasar por el menú de consola.

Cada endpoint traduce las excepciones ya definidas en la capa de servicios
(ValueError, PermissionError, KeyError, RuntimeError) a códigos de estado HTTP.
"""

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from servicios.sistema_electoral import SistemaElectoral
from servicios import analitica
from esquemas import VerificarDniRequest, VotoRequest

app = FastAPI(title="Sistema Electoral Digital - API")

# Habilita al frontend (otro origen/puerto) a llamar esta API desde el navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia única compartida por todas las peticiones (mismo rol que en main.py).
sistema = SistemaElectoral()


@app.get("/api/health")
def salud():
    """Chequeo simple de disponibilidad de la API."""
    return {"status": "ok"}


@app.post("/api/auth/verificar")
def verificar_identidad(payload: VerificarDniRequest):
    """Valida que el DNI exista en el padrón y no haya votado todavía."""
    try:
        sistema.auth_service.verificar_identidad(payload.dni)
        return {"dni": payload.dni, "verificado": True}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/candidatos")
def listar_candidatos():
    """Lista los candidatos disponibles (incluye 'Voto en Blanco')."""
    try:
        sistema.cargar_candidatos()
        return [
            {"id": c.id, "nombre": c.nombre, "partido": c.partido}
            for c in sistema.candidatos.values()
        ]
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/api/votos", status_code=201)
def emitir_voto(payload: VotoRequest):
    """Registra el voto de un DNI para un candidato.

    Vuelve a verificar la identidad aquí (y no solo en /auth/verificar) porque
    una API es stateless: nada impide que alguien llame este endpoint
    directamente sin haber pasado antes por la verificación.
    """
    try:
        sistema.auth_service.verificar_identidad(payload.dni)
        sistema.registrar_voto(payload.dni, payload.id_candidato)
        return {"mensaje": "Voto registrado correctamente."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except KeyError as e:
        # KeyError.__str__ envuelve el mensaje entre comillas simples; se limpian para el cliente.
        raise HTTPException(status_code=404, detail=str(e).strip("'"))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/resultados")
def obtener_resultados():
    """Total de votos emitidos y porcentaje por candidato (Paradigma Funcional vía analitica.py)."""
    try:
        sistema.cargar_candidatos()
        lista = list(sistema.candidatos.values())
        return {
            "total": analitica.calcular_total_votos(lista),
            "reporte": analitica.generar_reporte_porcentajes(lista),
        }
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
