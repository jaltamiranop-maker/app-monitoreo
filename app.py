import streamlit as st
import requests
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generar_pdf(cliente, data_tabla):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=40, rightMargin=40)
    elements = []
    styles = getSampleStyleSheet()

    # --- ENCABEZADO ESTILO ORDEN DE PEDIDO ---
    elements.append(Paragraph(f"ORDEN DE PEDIDO N° 0001", styles['Title']))
    
    # Datos del Cliente en una tabla de 2 columnas
    datos_cliente_table = [
        [f"<b>Cliente:</b> {cliente['nombre']}", f"<b>Proyecto:</b> {cliente['proyecto']}"],
        [f"<b>Fecha:</b> {cliente['fecha']}", "<b>Ubicación:</b> PLANTA MANUELITA PALMIRA"]
    ]
    t_cli = Table(datos_cliente_table, colWidths=[260, 260])
    t_cli.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BACKGROUND', (0,0), (0,1), colors.whitesmoke)
    ]))
    elements.append(t_cli)
    elements.append(Spacer(1, 20))

    # --- TABLA DE DISTRIBUCIÓN DE PANELES ---
    elements.append(Paragraph("<b>DISTRIBUCIÓN Y DETALLE DE CORTES</b>", styles['Heading3']))
    header = ["Panel #", "Tamaño (mm)", "Cortes (mm)", "Desperdicio (mm)"]
    tabla_data = [header]
    
    for fila in data_tabla:
        tabla_data.append([fila["Panel"], fila["Tamaño"], fila["Cortes"], fila["Desperdicio"]])

    t_resumen = Table(tabla_data, colWidths=[60, 100, 260, 100])
    t_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#004a99")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    elements.append(t_resumen)
    elements.append(Spacer(1, 20))

    # --- GRÁFICOS DE CORTE PARA OPERARIOS ---
    elements.append(Paragraph("<b>GUÍA VISUAL PARA CORTE</b>", styles['Heading3']))
    
    for fila in data_tabla:
        # Dibujo del panel
        d = Drawing(500, 50)
        ancho_total = 500  # Representa el 100% del panel en el dibujo
        longitud_panel = fila["Tamaño"]
        
        # Dibujar el panel base (Gris claro)
        d.add(Rect(0, 10, ancho_total, 30, fillColor=colors.lightgrey))
        
        # Dibujar cada corte (Azul Kingspan)
        cortes_lista = [int(x.strip()) for x in str(fila["Cortes"]).split(",")]
        x_actual = 0
        for corte in cortes_lista:
            ancho_corte = (corte / longitud_panel) * ancho_total
            d.add(Rect(x_actual, 10, ancho_corte, 30, fillColor=colors.HexColor("#004a99")))
            d.add(String(x_actual + 2, 15, f"{corte}mm", fontSize=7, fillColor=colors.white))
            x_actual += ancho_corte
            
        # Etiqueta del panel
        elements.append(Paragraph(f"Panel {fila['Panel']} ({fila['Tamaño']} mm)", styles['Normal']))
        elements.append(d)
        elements.append(Spacer(1, 10))

    doc.build(elements)
    buffer.seek(0)
    return buffer

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

# --- BARRA LATERAL: DATOS DEL CLIENTE ---
st.sidebar.header("👤 Datos del Cliente")
nombre_cliente = st.sidebar.text_input("Nombre / Empresa")
proyecto_cliente = st.sidebar.text_input("Nombre del Proyecto")
fecha_actual = st.sidebar.date_input("Fecha de Entrega")

cliente_dict = {
    "nombre": nombre_cliente,
    "proyecto": proyecto_cliente,
    "fecha": str(fecha_actual)
}

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
                    # --- BOTÓN DE DESCARGA PDF ---
                    st.markdown("### 🖨️ Exportar Resultados")
                    pdf_file = generar_pdf(cliente_dict, data)
    
                    st.download_button(
                    label="📥 Descargar Reporte en PDF",
                    data=pdf_file,
                    file_name=f"Cortes_{nombre_cliente}_{fecha_actual}.pdf",
                    mime="application/pdf",
                    key="pdf_download"
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