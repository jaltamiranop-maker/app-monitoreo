from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Any
from optimizer import optimize_cutting, format_output
from infrastructure.database import (
    iniciar_db, obtener_siguiente_orden, guardar_pedido,
    consultar_historial, obtener_detalle_pedido
)
from infrastructure.pdf_generator import generar_pdf
import json

app = FastAPI(title="Kingspan Optimizer API")

# ── CORS: permite que el frontend React (cualquier origen en desarrollo) llame a la API ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # En producción, reemplaza "*" con la URL exacta del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar base de datos al arrancar
iniciar_db()


# ── MODELOS ────────────────────────────────────────────────────────────────────

class Corte(BaseModel):
    longitud: int
    cantidad: int

class OptimizarRequest(BaseModel):
    cortes: list[Corte]

class GuardarRequest(BaseModel):
    datos_pdf: dict[str, Any]
    resultado: list[dict[str, Any]]


# ── ENDPOINTS ──────────────────────────────────────────────────────────────────

@app.get("/siguiente_orden")
def siguiente_orden():
    """Retorna el próximo número de orden disponible."""
    return {"siguiente": obtener_siguiente_orden()}


@app.post("/optimizar")
def optimizar(data: OptimizarRequest):
    """Corre el algoritmo de optimización y retorna el detalle por panel."""
    resultado = optimize_cutting(data.cortes)
    return format_output(resultado)


@app.post("/guardar_pedido")
def guardar_pedido_endpoint(data: GuardarRequest):
    """Guarda el pedido en la base de datos SQLite."""
    guardar_pedido(
        cliente=data.datos_pdf.get("cliente", ""),
        producto=data.datos_pdf.get("producto", ""),
        datos_dict=data.datos_pdf,
        resultado_list=data.resultado,
    )
    return {"ok": True}


@app.post("/generar_pdf")
def generar_pdf_endpoint(data: GuardarRequest):
    """Genera y retorna el PDF de la orden como archivo descargable."""
    buffer = generar_pdf(data.datos_pdf, data.resultado)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="Orden_{data.datos_pdf.get("n_orden","0000")}.pdf"'
            )
        },
    )


@app.get("/historial")
def historial():
    """Retorna el historial de órdenes guardadas."""
    df = consultar_historial()
    return df.to_dict(orient="records")


@app.post("/regenerar_pdf/{id_pedido}")
def regenerar_pdf(id_pedido: int):
    """Regenera el PDF de una orden ya guardada en la base de datos."""
    info_cliente, info_cortes = obtener_detalle_pedido(id_pedido)
    if not info_cliente or not info_cortes:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    buffer = generar_pdf(info_cliente, info_cortes)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="Orden_{id_pedido:04d}.pdf"'
        },
    )
