import streamlit as st
import requests
import base64
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
import datetime
from reportlab.platypus import Image as RLImage
import streamlit as st
from database import iniciar_db, obtener_siguiente_orden, guardar_pedido
from database import consultar_historial

 
# Inicializamos la base de datos al arrancar
iniciar_db()

def get_gif_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

gif_base64 = get_gif_base64("LeoSaludando.gif")
# --- LÓGICA DEL NÚMERO DE ORDEN ---
# Consultamos el siguiente número disponible
siguiente_n_orden = obtener_siguiente_orden()

def generar_pdf(info, data_tabla):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=20)
    elements = []
    styles = getSampleStyleSheet()
    
    # --- LOGO Y TÍTULO ---
    # Intentamos cargar el logo (debe estar en la misma carpeta)
    header_table = [[Paragraph(f"<font size=14>ORDEN DE PRODUCCIÓN N° {info['n_orden']}</font>", styles['Title'])]]
    t_header = Table(header_table, colWidths=[150, 350])
    t_header.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    elements.append(t_header)
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#c5a367")))
    elements.append(Spacer(1, 15))

    # --- TABLA DE DATOS DEL CLIENTE Y PROYECTO ---
    data_cliente = [
        [Paragraph(f"<b>Cliente:</b> {info['cliente']}", styles['Normal']), Paragraph(f"<b>NIT:</b> {info['nit']}", styles['Normal'])],
        [Paragraph(f"<b>Contacto:</b> {info['contacto']}", styles['Normal']), Paragraph(f"<b>Teléfono:</b> {info['telefono']}", styles['Normal'])],
        [Paragraph(f"<b>Comercial:</b> {info['comercial']}", styles['Normal']), Paragraph(f"<b>Producto:</b> {info['producto']}", styles['Normal'])],
        [Paragraph(f"<b>Transporte:</b> {info['transporte']}", styles['Normal']), Paragraph(f"<b>Ciudad:</b> {info['ciudad']}", styles['Normal'])],
        [Paragraph(f"<b>Dirección:</b> {info['direccion']}", styles['Normal']), Paragraph(f"<b>F. Entrega:</b> {info['f_entrega']}", styles['Normal'])]
    ]
    t_cli = Table(data_cliente, colWidths=[250, 250])
    t_cli.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
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
        st.info("Configura los cortes y los datos del cliente para generar una nueva orden.")        
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

                    if not cliente or not nit:
                        st.error("Por favor completa los datos del cliente en la barra lateral antes de optimizar.")
                    else:
                        data_opt = data
                        guardar_pedido(cliente, producto, datos_pdf, data_opt)
                        st.success("Orden guardada correctamente.")

                        datos_pdf["n_orden"] = f"{siguiente_n_orden:04d}"
                        pdf_final = generar_pdf(datos_pdf, data_opt)
                        st.download_button("📥 Descargar Orden", pdf_final, f"Orden_{siguiente_n_orden}.pdf")
                        st.download_button(
                            label="📥 DESCARGAR ORDEN Y FINALIZAR",
                            data=pdf_final,
                            file_name=f"Orden_{siguiente_n_orden:04d}_{cliente}.pdf",
                            mime="application/pdf")
                        st.success(f"Pedido N° {siguiente_n_orden} guardado en base de datos.")
                else:
                    st.error(f"Error en la optimización: {response.status_code}")
            except Exception as e:
                st.error(f"Error al calcular la optimización: {e}")

    with tab_historial:
        st.subheader("📜 Historial y Recuperación de PDF")
        
        try:
            df_historial = consultar_historial()
            
            if not df_historial.empty:
                # 1. Mostrar la tabla de historial
                st.dataframe(df_historial, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.write("### ⬇️ Re-descargar Orden")
                
                # 2. Selector para elegir qué orden recuperar
                id_a_recuperar = st.selectbox(
                    "Selecciona el N° de Orden para regenerar el PDF:",
                    df_historial['N° Orden'].tolist()
                )
                
                if st.button(f"Generar PDF de la Orden {id_a_recuperar}"):
                    with st.spinner("Reconstruyendo documento..."):
                        # Obtener datos de la DB
                        info_cliente, info_cortes = data_opt(id_a_recuperar)
                        
                        if info_cliente and info_cortes:
                            # Usamos la misma función de PDF que ya tenemos
                            pdf_recuperado = generar_pdf(info_cliente, info_cortes)
                            
            else:
                st.info("No hay órdenes en el historial.")

        except Exception as e:
            st.error(f"🚨 Error crítico: {e}")
         
        
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

