from fastapi import FastAPI
from pydantic import BaseModel
from backend.optimizer import optimize_cutting, format_output


app = FastAPI()


class Corte(BaseModel):
    longitud: int
    cantidad: int


class RequestModel(BaseModel):
    cortes: list[Corte]


@app.post("/optimizar")
def optimizar(data: RequestModel):
    resultado = optimize_cutting(data.cortes)
    return format_output(resultado)
