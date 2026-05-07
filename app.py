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
import datetime
from reportlab.platypus import Image as RLImage
import streamlit as st
from database import iniciar_db, obtener_siguiente_orden, guardar_pedido
from database import consultar_historial
from database import obtener_detalle_pedido

 
# Inicializamos la base de datos al arrancar
iniciar_db()

# --- LÓGICA DEL NÚMERO DE ORDEN ---
# Consultamos el siguiente número disponible
siguiente_n_orden = obtener_siguiente_orden()

def generar_pdf(info, data_tabla):
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle,
        Paragraph, Spacer
    )
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.styles import ParagraphStyle
    from io import BytesIO

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=15,
        leftMargin=15,
        rightMargin=15,
        bottomMargin=15
    )

    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        'titulo',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        textColor=colors.white,
        fontSize=20,
        leading=24
    )

    normal_center = ParagraphStyle(
        'normal_center',
        parent=styles['BodyText'],
        alignment=TA_CENTER,
        fontSize=9
    )

    azul = colors.HexColor("#003B8E")

    elements = []

    # =========================================================
    # HEADER PRINCIPAL
    # =========================================================

    header = Table([
        [
            Paragraph("<b>ORDEN DE PEDIDO</b>", titulo_style),
            Paragraph(
                f"<b>N° ORDEN<br/>{info['n_orden']}</b>",
                titulo_style
            )
        ]
    ], colWidths=[420, 110])

    header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), azul),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 18),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
    ]))

    elements.append(header)
    elements.append(Spacer(1, 10))

    # =========================================================
    # DATOS CLIENTE
    # =========================================================

    datos_cliente = [
        ["Cliente:", info["cliente"], "Proyecto:", ""],
        ["Nombre Contacto:", info["contacto"], "N° Teléfono Obra:", info["telefono"]],
        ["Teléfono Contacto:", info["telefono"], "E-Mail Contacto:", info["correo"]],
        ["Tipo de Destino:", info["tipo_destino"], "Tipo de Obra:", info["mercado"]],
        ["Ubicación Proyecto:", info["ciudad"], "Tipo de Proyecto:", "NUEVA CONSTRUCCIÓN"],
        ["Dirección Entrega:", info["direccion"], "Transporte a Cargo de:", info["transporte"]],
        ["Fecha compromiso entrega en Planta:", info["f_entrega"], "", ""],
    ]

    tabla_cliente = Table(
        datos_cliente,
        colWidths=[110, 160, 110, 150]
    )

    tabla_cliente.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), azul),
        ('BACKGROUND', (2, 0), (2, 5), azul),

        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('TEXTCOLOR', (2, 0), (2, 5), colors.white),

        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),

        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('SPAN', (1, 6), (3, 6)),
    ]))

    elements.append(tabla_cliente)
    elements.append(Spacer(1, 15))

    # =========================================================
    # RESUMEN SUPERIOR
    # =========================================================

    area_total = 0
    total_unidades = 0

    for fila in data_tabla:
        cortes = [int(x.strip()) for x in str(fila["Cortes"]).split(",")]
        area_total += sum(cortes) / 1000
        total_unidades += len(cortes)

    resumen_superior = Table([
        [
            Paragraph("<b>TIPO DE PRODUCTO</b><br/><br/>PANEL", titulo_style),

            Table([
                ["Longitud\n(mm)", "Unidades", "Área\n(m²)"],
                ["9.000", str(total_unidades), f"{area_total:.2f}"]
            ], colWidths=[90, 90, 90]),

            Table([
                ["RESUMEN", ""],
                ["Área Requerida:", f"{area_total:.2f} m²"],
                ["Área Suministrada:", f"{area_total:.2f} m²"],
                ["Desperdicio Total:", "0.00 m²"]
            ], colWidths=[120, 120])
        ]
    ], colWidths=[120, 280, 240])

    resumen_superior.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))

    elements.append(resumen_superior)
    elements.append(Spacer(1, 15))

    # =========================================================
    # TABLAS CENTRALES
    # =========================================================

    cortes_data = [["Corte", "Unidades", "Requerido", "Suministrado"]]

    for fila in data_tabla:
        cortes_lista = [int(x.strip()) for x in str(fila["Cortes"]).split(",")]

        for corte in cortes_lista:
            cortes_data.append([
                f"{corte} mm",
                "1",
                f"{corte/1000:.2f} m²",
                f"{corte/1000:.2f} m²"
            ])

    cortes_data.append([
        "TOTAL",
        str(total_unidades),
        f"{area_total:.2f} m²",
        f"{area_total:.2f} m²"
    ])

    tabla_cortes = Table(cortes_data, colWidths=[70, 60, 90, 90])

    tabla_cortes.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), azul),
        ('BACKGROUND', (0, -1), (0, -1), azul),

        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, -1), (0, -1), colors.white),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))

    desperdicio = Table([
        ["Longitud", "Unidades", "m²"],
        ["0 mm", "0", "0.00"],
        ["0 mm", "0", "0.00"],
        ["TOTAL", "0", "0.00"]
    ], colWidths=[90, 70, 70])

    desperdicio.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), azul),
        ('BACKGROUND', (0, -1), (0, -1), azul),

        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, -1), (0, -1), colors.white),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))

    distribucion = [["Panel", "Tamaño", "Corte 1", "Desperdicio"]]

    contador = 1

    for fila in data_tabla:
        cortes_lista = [int(x.strip()) for x in str(fila["Cortes"]).split(",")]

        for corte in cortes_lista:
            desperdicio_mm = 12000 - corte

            distribucion.append([
                str(contador),
                "12000",
                str(corte),
                str(desperdicio_mm)
            ])

            contador += 1

    tabla_distribucion = Table(
        distribucion,
        colWidths=[45, 70, 70, 80]
    )

    tabla_distribucion.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), azul),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))

    centro = Table([
        [tabla_cortes, desperdicio, tabla_distribucion]
    ], colWidths=[240, 180, 265])

    elements.append(centro)
    elements.append(Spacer(1, 20))

    # =========================================================
    # PARTE INFERIOR
    # =========================================================
    
    # Extraemos la tabla que el usuario editó en la interfaz web, si no existe ponemos una vacía por seguridad
    tabla_log_usuario = info.get("servicio_logistico_tabla", [
        {"Concepto": "SERVICIO LOGÍSTICO", "Tipo": "MINIMULA", "Cantidad": 1.0, "Precio_COP": 0},
        {"Concepto": "", "Tipo": "", "Cantidad": 0.0, "Precio_COP": 0}
    ])
    
    # Formateamos los números a strings con separadores de miles y signo $ para el PDF
    f1_cant = f"{tabla_log_usuario[0]['Cantidad']:,.2f}"
    f1_cop = f"${tabla_log_usuario[0]['Precio_COP']:,.0f}" if tabla_log_usuario[0]['Precio_COP'] > 0 else "$0"
    
    f2_cant = f"{tabla_log_usuario[1]['Cantidad']:,.2f}"
    f2_cop = f"${tabla_log_usuario[1]['Precio_COP']:,.0f}" if tabla_log_usuario[1]['Precio_COP'] > 0 else "$0"

    # Estructuramos la matriz exactamente igual al diseño de la imagen original
    servicio = Table([
        ["SERVICIO LOGÍSTICO", ""],
        ["Tipo", str(tabla_log_usuario[0]["Tipo"])],
        ["Cantidad", f1_cant],
        ["COP $", f1_cop],
        ["", ""], # Fila divisoria intermedia
        ["Tipo", str(tabla_log_usuario[1]["Tipo"])],
        ["Cantidad", f2_cant],
        ["COP $", f2_cop],
    ], colWidths=[120, 120])
    
    # Aplicamos estilos específicos para combinar celdas de títulos como en la imagen
    servicio.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),  # Une "SERVICIO LOGÍSTICO"
        ('SPAN', (0, 4), (1, 4)),  # Une la fila vacía del medio
        ('BACKGROUND', (0, 0), (-1, 0), azul),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # --- RE-CALCULAR EL TOTAL DE LA ORDEN DE FORMA REAL ---
    # Sumamos el costo logístico real al total de la orden en lugar del estático 4600000
    costo_logistico_total = sum(item['Cantidad'] * item['Precio_COP'] for item in tabla_log_usuario)
    total_orden = 4600000 + costo_logistico_total # Puedes cambiar la base de 4600000 según tus productos

    kits = Table([
        ["KITS DE FIJACIÓN", ""],
        ["Tipo", ""],
        ["Cantidad", ""],
        ["COP $", ""],
        ["", ""],
        ["Tipo", ""],
        ["Cantidad", ""],
        ["COP $", ""],
    ], colWidths=[120, 120])

    totales = Table([
        ["TOTALES", ""],
        ["Área Requerida:", f"{area_total:.2f} m²"],
        ["Área Suministrada:", f"{area_total:.2f} m²"],
        ["Desperdicio Total:", "0.00 m²"],
        ["TOTAL ORDEN", ""],
        [f"${total_orden:,.0f}", "COP"]
    ], colWidths=[140, 120])

    for tabla in [servicio, kits, totales]:
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), azul),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))

    inferior = Table([
        [servicio, kits, totales]
    ], colWidths=[240, 240, 260])

    elements.append(inferior)
    elements.append(Spacer(1, 20))

    # =========================================================
    # OBSERVACIONES
    # =========================================================

    observaciones = Table([
        ["OBSERVACIONES:"],
        [""],
        [""]
    ], colWidths=[740])

    observaciones.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), azul),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ROWHEIGHT', (1, 1), (-1, -1), 40),
    ]))

    elements.append(observaciones)

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
    # Sección 3: Logística y Entrega
    with st.expander("Logística y Entrega"):
        sector = st.text_input("Sector")
        mercado = st.selectbox("Mercado Final", ["Escoge mercado","Nuevo", "Remodelación"])
        canal = st.selectbox("Canal de Venta", ["Escoge canal","Cliente final","Distribuidor"])
        tipo_destino = st.selectbox("Tipo Destino", ["Escoge una opción","Venta con IVA", "Exportación"])
        transporte = st.selectbox("Transporte", ["Escoge una opción","Kingspan", "Cliente"])
        
        # --- MODIFICACIÓN AQUÍ ---
        # Inicializamos variables por defecto
        servicio_logistico = "No aplica"
        ciudad = ""
        
        if transporte == "Kingspan":
            # Cambiamos las opciones a MAYÚSCULAS para que coincida exactamente con tu imagen (MINIMULA)
            servicio_logistico = st.selectbox("Servicio Logístico", ["Escoge una opción", "MINIMULA", "SENCILLO", "TURBO"])
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

                    # =========================================================
                    # NUEVA SECCIÓN: TABLA INTERACTIVA DE SERVICIO LOGÍSTICO
                    # =========================================================
                    st.markdown("---")
                    st.subheader("🚚 Datos del Servicio Logístico")
                    
                    # Inicializamos los datos por defecto para la tabla interactiva
                    # Si el transporte es del cliente, dejamos valores vacíos.
                    tipo_tabla = servicio_logistico if transporte == "Kingspan" else "N/A"
                    
                    # Creamos la estructura idéntica a tu imagen (2 filas de servicio)
                    raw_logistica_data = [
                        {"Concepto": "SERVICIO LOGÍSTICO", "Tipo": tipo_tabla, "Cantidad": 1.00, "Precio_COP": 2800000},
                        {"Concepto": "", "Tipo": "", "Cantidad": 0.00, "Precio_COP": 0}
                    ]
                    
                    df_logistica = pd.DataFrame(raw_logistica_data)
                    
                    # Configuración de las columnas para bloquear "Concepto" y "Tipo", y formatear "COP $"
                    config_columnas = {
                        "Concepto": st.column_config.TextColumn("Concepto", disabled=True, width="medium"),
                        "Tipo": st.column_config.TextColumn("Tipo", disabled=True, width="medium"),
                        "Cantidad": st.column_config.NumberColumn("Cantidad", min_value=0.0, format="%.2f", step=1.0),
                        "Precio_COP": st.column_config.NumberColumn(
                            "COP $", 
                            min_value=0, 
                            format="$%d", # El signo $ se vuelve nativo y no se puede borrar
                            step=50000
                        )
                    }
                    
                    st.write("Completa los valores de cantidad y costos para la orden:")
                    # Guardamos los cambios que haga el usuario en una variable
                    tabla_editada = st.data_editor(
                        df_logistica, 
                        column_config=config_columnas, 
                        use_container_width=True, 
                        hide_index=True,
                        num_rows="fixed"
                    )
                    
                    # Convertimos la tabla editada a una lista de diccionarios para pasarla al PDF y a la DB
                    datos_servicio_guardar = tabla_editada.to_dict(orient="records")
                    st.markdown("---")

                    # Validamos datos del cliente antes de proceder a la descarga
                    if not cliente or not nit:
                        st.error("Por favor completa los datos del cliente en la barra lateral antes de optimizar.")
                    elif transporte == "Kingspan" and servicio_logistico == "Escoge una opción":
                        st.error("Por favor selecciona un Tipo de Servicio Logístico válido en la barra lateral.")
                    else:
                        data_opt = data
                        
                        # Añadimos los datos de la tabla logística editada al diccionario general de la orden
                        datos_pdf["servicio_logistico_tabla"] = datos_servicio_guardar
                        
                        # Guardamos en la base de datos (tu función actual)
                        guardar_pedido(cliente, producto, datos_pdf, data_opt)
                        st.success("Orden guardada correctamente.")

                        datos_pdf["n_orden"] = f"{siguiente_n_orden:04d}"
                        
                        # --- PASAMOS LA TABLA EDITADA A LA FUNCIÓN GENERAR_PDF ---
                        pdf_final = generar_pdf(datos_pdf, data_opt)
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            st.download_button("📥 Descargar Orden", pdf_final, f"Orden_{siguiente_n_orden}.pdf")
                        with col_btn2:
                            st.download_button(
                                label="📥 DESCARGAR ORDEN Y FINALIZAR",
                                data=pdf_final,
                                file_name=f"Orden_{siguiente_n_orden:04d}_{cliente}.pdf",
                                mime="application/pdf"
                            )
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
                        info_cliente, info_cortes = obtener_detalle_pedido(id_a_recuperar)
                        
                        if info_cliente and info_cortes:
                            # Usamos la misma función de PDF que ya tenemos
                            pdf_recuperado = generar_pdf(info_cliente, info_cortes)
                            
            else:
                st.info("No hay órdenes en el historial.")

        except Exception as e:
            st.error(f"🚨 Error crítico: {e}")
         
        
# Pie de página responsivo
st.markdown("""
    <div style='text-align: center; color: #888; padding-top: 50px;'>
        <small>© 2026 Kingspan Optimization Tools</small>
    </div>
    """, unsafe_allow_html=True)

