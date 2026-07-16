import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from servicios.sistema_electoral import SistemaElectoral
from servicios import analitica
from esquemas import VerificarDniRequest, VotoRequest

app = FastAPI(title="Sistema Electoral Digital - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")],
    allow_methods=["*"],
    allow_headers=["*"],
)

sistema = SistemaElectoral()


@app.get("/api/health")
def salud():
    return {"status": "ok"}


@app.post("/api/auth/verificar")
def verificar_identidad(payload: VerificarDniRequest):
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
    try:
        sistema.auth_service.verificar_identidad(payload.dni)
        sistema.registrar_voto(payload.dni, payload.id_candidato)
        return {"mensaje": "Voto registrado correctamente."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e).strip("'"))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/api/resultados")
def obtener_resultados():
    try:
        sistema.cargar_candidatos()
        lista = list(sistema.candidatos.values())
        return {
            "total": analitica.calcular_total_votos(lista),
            "reporte": analitica.generar_reporte_porcentajes(lista),
        }
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
