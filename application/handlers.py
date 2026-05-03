from infrastructure.api_client import optimizar_cortes_api
from infrastructure.pdf_generator import generar_pdf
from infrastructure.database import guardar_pedido
import infrastructure.pdf_generator as test
print(dir(test))

def handle_optimizar(cortes):
    if not cortes:
        return {"error": "No hay cortes válidos"}

    try:
        data = optimizar_cortes_api(cortes)
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}
    

def handle_generar_pdf(info, data):
    try:
        pdf = generar_pdf(info, data)
        return {"pdf": pdf}
    except Exception as e:
        return {"error": str(e)}

def handle_guardar(cliente, producto, datos, resultado):
    try:
        guardar_pedido(cliente, producto, datos, resultado)
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}