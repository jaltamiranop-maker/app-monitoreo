import streamlit as st
import requests

# Configuración de la página
st.set_page_config(
    page_title="Kingspan | Optimizador de Cortes",
    page_icon="🦁",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    /* Colores Kingspan: Azul #004a99, Dorado #c5a367 */
    .main {
        background-color: #ffffff;
    }
    .stApp {
        color: #004a99;
    }
    /* Estilo para el encabezado y logo */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 0rem;
        border-bottom: 3px solid #c5a367;
        margin-bottom: 2rem;
    }
    /* Botones personalizados */
    div.stButton > button:first-child {
        background-color: #004a99;
        color: white;
        border-radius: 5px;
        border: 2px solid #004a99;
        font-weight: bold;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background-color: #c5a367;
        border-color: #c5a367;
        color: white;
    }
    /* Títulos y etiquetas */
    h1, h2, h3 {
        color: #004a99 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    /* Contenedores de entrada */
    .stNumberInput {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO CON LOGO ---
col_logo, col_text = st.columns([1, 3])
with col_logo:
    # Asegúrate de que el nombre del archivo coincida con el que subiste
    st.image("Logo Kingspan_editable-png.png", width=250)

with col_text:
    st.title("Optimizador de Cortes de Panel")
    st.caption("Herramienta de eficiencia para la gestión de materiales.")

st.markdown("---")

# --- CUERPO DE LA APP ---
col_input, col_spacer, col_table = st.columns([1, 0.1, 2])

with col_input:
    st.subheader("📋 Parámetros")
    rows = st.number_input("Tipos de corte", min_value=1, max_value=20, value=1)
    
    cortes = []
    
    with st.expander("Configurar Dimensiones", expanded=True):
        for i in range(rows):
            st.markdown(f"**Corte #{i+1}**")
            c1, c2 = st.columns(2)
            l = c1.number_input(f"Largo (mm)", key=f"l{i}", min_value=0)
            c = c2.number_input(f"Cant.", key=f"c{i}", min_value=0)
            
            if l > 0 and c > 0:
                cortes.append({"longitud": int(l), "cantidad": int(c)})

    btn_optimizar = st.button("🚀 CALCULAR OPTIMIZACIÓN")

with col_table:
    st.subheader("📊 Resultado del Cálculo")
    
    if btn_optimizar:
        if not cortes:
            st.warning("⚠️ Por favor, ingresa datos válidos de longitud y cantidad.")
        else:
            try:
                with st.spinner('Calculando mejor combinación...'):
                    response = requests.post(
                        "http://127.0.0.1:8000/optimizar",
                        json={"cortes": cortes}
                    )

                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Optimización completada con éxito")
                    
                    # --- NUEVA SECCIÓN: RESUMEN DE PANELES ---
                    st.markdown("### 📋 Resumen de Inventario")
                    
                    # Extraer los tamaños de los paneles usados
                    tamanos_usados = [row["Tamaño"] for row in data]
                    
                    # Definir los tamaños estándar de Kingspan
                    PANEL_SIZES = [12000, 9000, 6000, 3000]
                    
                    # Crear columnas para las métricas rápidas
                    met_cols = st.columns(len(PANEL_SIZES))
                    resumen_data = []

                    for i, tamaño in enumerate(PANEL_SIZES):
                        cantidad = tamanos_usados.count(tamaño)
                        resumen_data.append({"Tamaño (mm)": f"{tamaño}", "Cantidad Necesaria": cantidad})
                        # Mostrar métrica individual
                        met_cols[i].metric(f"{tamaño} mm", cantidad)

                    # Mostrar tabla de resumen estilizada
                    st.table(resumen_data)
                    
                    st.markdown("---")
                    
                    # --- DETALLE DE CORTES ---
                    st.markdown("### 🔍 Detalle por Panel")
                    st.dataframe(data, use_container_width=True)
                    
                    # Botón para descargar resultados (opcional pero muy útil)
                    csv = st.sidebar.download_button(
                        label="Descargar Reporte CSV",
                        data=str(data),
                        file_name="optimizacion_kingspan.csv",
                        mime="text/csv",
                    )

                else:
                    st.error("❌ Error en la conexión con el motor de cálculo (API)")

            except Exception as e:
                st.error(f"🚨 Error crítico: {e}")
    else:
        st.info("Ingresa los datos a la izquierda y presiona el botón para ver los resultados.")
        
        
        
# Pie de página responsivo
st.markdown("""
    <div style='text-align: center; color: #888; padding-top: 50px;'>
        <small>© 2026 Kingspan Optimization Tools</small>
    </div>
    """, unsafe_allow_html=True)