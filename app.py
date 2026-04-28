import streamlit as st
import requests


st.title("Optimizador de Cortes")


st.write("Ingresa longitudes y cantidades")


rows = st.number_input("Cantidad de tipos de corte", min_value=1, max_value=20, value=3)


cortes = []


for i in range(rows):
    col1, col2 = st.columns(2)


    longitud = col1.number_input(f"Longitud {i+1} (mm)", key=f"l{i}", min_value=0)
    cantidad = col2.number_input(f"Cantidad {i+1}", key=f"c{i}", min_value=0)


# 👇 construir lista DESPUÉS del loop
for i in range(rows):
    l = st.session_state.get(f"l{i}", 0)
    c = st.session_state.get(f"c{i}", 0)


    if l > 0 and c > 0:
        cortes.append({
            "longitud": int(l),
            "cantidad": int(c)
        })


if st.button("Optimizar"):


    try:
        # limpiar datos
        cortes_validos = []


        for c in cortes:
            if "longitud" in c and "cantidad" in c:
                if c["longitud"] > 0 and c["cantidad"] > 0:
                    cortes_validos.append({
                        "longitud": int(c["longitud"]),
                        "cantidad": int(c["cantidad"])
                    })


        if not cortes_validos:
            st.warning("No hay datos válidos")
        else:
            response = requests.post(
                "http://127.0.0.1:8000/optimizar",
                json={"cortes": cortes_validos}
            )


            if response.status_code == 200:
                data = response.json()
                st.success("Optimización completada")
                st.dataframe(data)
            else:
                st.error("Error en la API")


    except Exception as e:
        st.error(f"Error crítico: {e}")