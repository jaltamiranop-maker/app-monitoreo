import requests

def optimizar_cortes_api(cortes):
    response = requests.post(
        "http://127.0.0.1:8000/optimizar",
        json={"cortes": cortes}
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Error en API")