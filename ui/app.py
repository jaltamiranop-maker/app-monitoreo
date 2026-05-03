

import streamlit as st
import requests
import base64

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

#Importacion para POE
import datetime
from state.session import init_state
from infrastructure.database import obtener_siguiente_orden
from infrastructure.database import iniciar_db
#Manejadores de eventos
from application.handlers import handle_optimizar
from application.handlers import handle_generar_pdf
from application.handlers import handle_guardar


init_state()
if "resultado" not in st.session_state:
    st.session_state.resultado = None
iniciar_db()

siguiente_n_orden = obtener_siguiente_orden()

def get_gif_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

gif_base64 = get_gif_base64("Leo.gif")



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
    
    

    with col_text:
        st.title("Optimizador de Cortes de Panel")
        st.caption("Herramienta de eficiencia para la gestión de materiales.")
        

st.markdown("---")

# --- BARRA LATERAL: DATOS DEL CLIENTE ---
# --- CONFIGURACIÓN DE LA BARRA LATERAL ---
st.sidebar.image("Logo Kingspan_editable-png.png", use_container_width=True)
st.sidebar.title("📄 Datos de Producción")

with st.sidebar.form("formulario_orden"):
    # Sección 1: Información General
    with st.expander("Información de la Orden", expanded=True):
        f_despiece = st.date_input("Fecha de Despiece", value=datetime.date.today())
        n_orden = siguiente_n_orden
        comercial = st.selectbox("Comercial Asignado", ["Escoge Asesor","ALTAMIRANO PUENTES YAZMIN",
                    "ARENAS GUZMAN DIEGO FERNANDO",
                    "ARIAS GIRALDO ANA ISABEL",
                    "BENAVIDES MARQUEZ JULIO ALBERTO",
                    "CALDERON DIEGO",
                    "CANDELA YOLANDA",
                    "GARCIA RUIZ MONICA ALEXANDRA",
                    "GIRALDO ALZATE LINA MARCELA",
                    "GUERRERO JULIO",
                    "LOZANO TENORIO MARIA CAROLINA",
                    "MOJICA MONTALVO JESUS DAVID",
                    "NARANJO ALEXIS",
                    "PEREZ JOHANA",
                    "QUINTANA BARRIOS JAIRO ALONSO",
                    "SALAZAR EDWAR",
                    "VALENZUELA RONALD",
                    ])
        orden_compra = st.text_input("Orden de Compra")

    # Sección 2: Datos del Cliente
    with st.expander("Datos del Cliente"):
        cliente = st.text_input("Nombre del Cliente")
        nit = st.text_input("NIT")
        contacto = st.text_input("Contacto de Obra")
        telefono = st.text_input("Teléfono")
        correo = st.text_input("Correo electrónico")

    # Sección 3: Logística y Destino
    with st.expander("Logística y Entrega"):
        sector = st.text_input("Sector")
        mercado = st.selectbox("Mercado Final", ["Escoge mercado","Nuevo", "Remodelación"])
        canal = st.selectbox("Canal de Venta", ["Escoge canal","Cliente final","Distribuidor"])
        tipo_destino = st.selectbox("Tipo Destino", ["Escoge una opción","Venta con IVA", "Exportación"])
        transporte = st.selectbox("Transporte", ["Escoge una opción","Kingspan", "Cliente"])
        
        # Mostrar servicio logístico solo si es Kingspan
        servicio_logistico = ""
        if transporte == "Kingspan":
            servicio_logistico = st.selectbox("Servicio Logístico", ["Escoge una opción","Minimula", "Sencillo","Turbo",])
            
        ciudad = ""
        if transporte =="Kingspan":
            ciudad = st.text_input("Ciudad de Entrega")
            
        direccion = st.text_input("Dirección de Entrega")
        f_entrega = st.date_input("Fecha de Entrega")

    # Sección 4: Especificaciones del Producto
    with st.expander("Producto y Kit"):
        producto = st.selectbox("Producto", ["Escoge un producto",
            "KINGFRIGO PIR100 CAL28-9002/CAL28-9002",
            "KINGFRIGO PIR80 CAL28-9002/CAL28-9002",
            "KINGFRIGO PIR40 CAL28-9002/CAL28-9002",
            "KINGROOF PIR30 CAL28-9002/CAL28-9002",
            "KINGROOF PIR18 CAL28-9002/CAL28-9002",
            "KINGROOF PIR15 CAL28-9002/CAL28-9002"
        ])
        kit_anclaje = st.selectbox("Kit de Anclaje", ["Escoge una cubierta","Cubierta 30", "Cubierta 18", "Metalroof", "Otro"])
        cantidad_kit = st.number_input("Cantidad de Kits", min_value=0)
        
    # Botón para guardar datos del formulario
    st.info(f"Esta orden quedará registrada con el ID: {siguiente_n_orden}")
    
    submit_form = st.form_submit_button("Confirmar Datos y Registrar")

# Empaquetar datos para el PDF
datos_pdf = {
    "f_despiece": str(f_despiece), "n_orden": n_orden, "cliente": cliente, "nit": nit,
    "contacto": contacto, "telefono": telefono, "correo": correo, "comercial": comercial,
    "sector": sector, "mercado": mercado, "canal": canal, "orden_compra": orden_compra,
    "tipo_destino": tipo_destino, "transporte": transporte, "ciudad": ciudad,
    "direccion": direccion, "servicio_logistico": servicio_logistico, "f_entrega": str(f_entrega),
    "producto": producto, "kit": kit_anclaje, "cantidad_kit": cantidad_kit
}
# --- CUERPO PRINCIPAL CON PESTAÑAS ---
tab_optimizador, tab_historial = st.tabs(["🚀 Optimizador de Cortes", "📜 Historial de Órdenes"])

# --- CUERPO DE LA APP ---
with tab_optimizador:
    col_input, col_spacer, col_table = st.columns([1, 0.05, 2])
    
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
        btn_optimizar = st.button("🚀 CALCULAR OPTIMIZACIÓN",use_container_width=True)

    with col_table:
        st.subheader("📊 Resultado del Cálculo")
    
    if btn_optimizar:
        st.session_state.resultado = handle_optimizar(cortes)
    else:
        st.info("Ingresa los datos a la izquierda y presiona el botón para ver los resultados.")
    
    
    
    resultado = st.session_state.get("resultado", None)
    print("RESULTADO:", resultado)
    print("TIPO:", type(resultado))
    data = None

    if resultado is None:
        st.info("Ejecuta la optimización para ver resultados.")
    else:
        if isinstance(resultado, dict) and "error" in resultado:
            st.error(resultado["error"])
        else:
            data = resultado.get("data") if isinstance(resultado, dict) else None

        if data:
            st.success("✅ Optimización completada")
            st.dataframe(data)
        else:
            st.warning("No hay datos para mostrar")

    if st.button("Guardar Pedido"):
        res = handle_guardar(cliente, producto, datos_pdf, data)
        
        if isinstance(resultado, dict) and "error" in resultado:
            st.error(resultado["error"])
        else:
            st.success("Pedido guardado correctamente")

    if st.button("📥 Descargar PDF"):
        res_pdf = handle_generar_pdf(cliente, data)
        
        if not res_pdf:
            st.error("No se pudo generar el PDF")
        elif "error" in res_pdf:
            st.error(res_pdf["error"])
        else:
            st.download_button(
                label="Descargar PDF",
                data=res_pdf["pdf"],
                file_name="orden.pdf",
                mime="application/pdf"
            )
        
        
        
# Pie de página responsivo
st.markdown(f"""
<style>
.mascota-container {{
    position: fixed;
    bottom: 20px;
    right: 20px !important;  /* 👉 derecha */
    left: auto !important;   /* 👉 evita que se vaya a la izquierda */
    width: 140px;
    z-index: 9999;
}}

.mascota-container img {{
    width: 100%;
    height: auto;
}}
</style>

<div class="mascota-container">
    <img src="data:image/gif;base64,{gif_base64}">
</div>
""", unsafe_allow_html=True)