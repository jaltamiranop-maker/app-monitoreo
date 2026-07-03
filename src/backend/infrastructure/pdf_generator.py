"""
pdf_generator.py
Genera el PDF de una orden de pedido Kingspan.
Extraído de app.py para ser reutilizable desde el backend FastAPI.
"""

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line

AZUL = colors.HexColor("#003B8E")
VERDE = colors.HexColor("#D6EFD9")
GRIS_CLARO = colors.HexColor("#F2F2F2")
BLANCO = colors.white

# Ancho útil de la página carta con márgenes de 15pt a cada lado
MARGEN = 15
ANCHO_UTIL = letter[0] - 2 * MARGEN  # 582pt
ANCHO = 580  # margen de seguridad de 2pt


# ── ESTILOS ──────────────────────────────────────────────────────────────────
def _titulo_style():
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        "titulo", parent=styles["Heading1"], alignment=TA_CENTER,
        textColor=colors.white, fontSize=18, leading=22,
    )


def _subtitulo_style():
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        "subtitulo", parent=styles["Heading2"], alignment=TA_CENTER,
        textColor=colors.white, fontSize=10, leading=13,
    )


def _texto_style(size=8, bold=False, color=colors.black, align=TA_CENTER):
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        f"texto_{size}_{bold}_{align}", parent=styles["BodyText"],
        alignment=align, fontSize=size, leading=size + 2,
        fontName="Helvetica-Bold" if bold else "Helvetica", textColor=color,
    )


def _total_style():
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        "total", parent=styles["Heading1"], alignment=TA_CENTER,
        textColor=AZUL, fontSize=20, leading=24, fontName="Helvetica-Bold",
    )


# ── ICONOS VECTORIALES ────────────────────────────────────────────────────────
def _icono_camion(color=AZUL, w=36, h=28):
    d = Drawing(w, h)
    d.add(Rect(1, 9, 15, 11, fillColor=color, strokeColor=None))
    d.add(Rect(16, 13, 17, 7, fillColor=color, strokeColor=None))
    d.add(Circle(9, 8, 3.5, fillColor=BLANCO, strokeColor=color, strokeWidth=1.4))
    d.add(Circle(27, 8, 3.5, fillColor=BLANCO, strokeColor=color, strokeWidth=1.4))
    return d


def _icono_tornillo(color=AZUL, w=26, h=30):
    d = Drawing(w, h)
    d.add(Circle(13, 24, 5.5, fillColor=color, strokeColor=None))
    d.add(Line(8.5, 24, 17.5, 24, strokeColor=BLANCO, strokeWidth=1.3))
    d.add(Rect(10.5, 3, 5, 17, fillColor=color, strokeColor=None))
    for y in (6, 10, 14):
        d.add(Line(8.5, y, 17.5, y, strokeColor=BLANCO, strokeWidth=0.8))
    return d


def generar_pdf(info: dict, data_tabla: list) -> BytesIO:
    """
    Genera un PDF con la orden de pedido.

    Args:
        info: Diccionario con todos los datos del formulario/cliente.
        data_tabla: Lista de dicts con claves Panel, Tamaño, Cortes, Desperdicio.

    Returns:
        BytesIO con el contenido del PDF listo para transmitir.
    """
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=MARGEN, leftMargin=MARGEN, rightMargin=MARGEN, bottomMargin=MARGEN,
    )

    titulo_style = _titulo_style()
    elements = []

    # ── HEADER ───────────────────────────────────────────────────────────────
    header = Table(
        [[
            Paragraph("<b>ORDEN DE PEDIDO</b>", titulo_style),
            Paragraph(f"<b>N° ORDEN<br/>{info.get('n_orden', '0000')}</b>", titulo_style),
        ]],
        colWidths=[ANCHO * 0.78, ANCHO * 0.22],
    )
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 1, colors.white),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(header)
    elements.append(Spacer(1, 6))

    # ── DATOS CLIENTE ─────────────────────────────────────────────────────────
    datos_cliente = [
        ["Cliente:", info.get("cliente", ""), "Proyecto:", info.get("proyecto", "")],
        ["Nombre Contacto:", info.get("contacto", ""), "N° Teléfono Obra:", info.get("telefono", "")],
        ["Teléfono Contacto:", info.get("telefono", ""), "E-Mail Contacto:", info.get("correo", "")],
        ["Tipo de Destino:", info.get("tipo_destino", ""), "Tipo de Obra:", info.get("mercado", "")],
        ["Ubicación Proyecto:", info.get("ciudad", ""), "Tipo de Proyecto:", "NUEVA CONSTRUCCIÓN"],
        ["Dirección Entrega:", info.get("direccion", ""), "Transporte a Cargo de:", info.get("transporte", "")],
        ["Fecha compromiso entrega en Planta:", info.get("f_entrega", ""), "", ""],
    ]

    col_cliente = [ANCHO * 0.21, ANCHO * 0.29, ANCHO * 0.21, ANCHO * 0.29]
    tabla_cliente = Table(datos_cliente, colWidths=col_cliente)
    tabla_cliente.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), AZUL),
        ("BACKGROUND", (2, 0), (2, 5), AZUL),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("TEXTCOLOR", (2, 0), (2, 5), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTNAME", (3, 0), (3, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("SPAN", (1, 6), (3, 6)),
    ]))
    elements.append(tabla_cliente)
    elements.append(Spacer(1, 6))

    # ── CÁLCULOS GENERALES ────────────────────────────────────────────────────
    cortes_por_fila = []
    area_total = 0
    total_unidades = 0
    for fila in data_tabla:
        cortes = [int(x.strip()) for x in str(fila["Cortes"]).split(",")]
        cortes_por_fila.append(cortes)
        area_total += sum(cortes) / 1000
        total_unidades += len(cortes)

    # ── RESUMEN SUPERIOR ──────────────────────────────────────────────────────
    tipo_producto = Table(
        [[Paragraph("<b>TIPO DE PRODUCTO</b><br/><br/><b>PANEL</b>", titulo_style)]],
        colWidths=[ANCHO * 0.19], rowHeights=[60],
    )
    tipo_producto.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 1, colors.white),
    ]))

    longitud_tbl = Table(
        [
            ["Longitud\n(mm)", "Unidades", "Área\n(m²)"],
            ["9.000", str(total_unidades), f"{area_total:.2f}"],
        ],
        colWidths=[ANCHO * 0.147] * 3, rowHeights=[30, 30],
    )
    longitud_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F5")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    resumen_box = Table(
        [
            ["RESUMEN", ""],
            ["Área Requerida:", f"{area_total:.2f} m²"],
            ["Área Suministrada:", f"{area_total:.2f} m²"],
            ["Desperdicio Total:", "0.00 m²"],
        ],
        colWidths=[ANCHO * 0.19, ANCHO * 0.19],
    )
    resumen_box.setStyle(TableStyle([
        ("SPAN", (0, 0), (1, 0)),
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GRIS_CLARO]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))

    resumen_superior = Table(
        [[tipo_producto, longitud_tbl, resumen_box]],
        colWidths=[ANCHO * 0.19, ANCHO * 0.44, ANCHO * 0.37],
    )
    resumen_superior.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(resumen_superior)
    elements.append(Spacer(1, 6))

    # ── TABLA CORTE (con encabezado de sección + columna Suministrado resaltada) ─
    cortes_data = [
        ["CORTE", "", "", ""],
        ["Corte", "Unidades", "Requerido (m²)", "Suministrado (m²)"],
    ]
    for cortes in cortes_por_fila:
        for corte in cortes:
            cortes_data.append([
                f"{corte} mm", "1",
                f"{corte / 1000:.2f} m²", f"{corte / 1000:.2f} m²",
            ])
    n_filas_corte = len(cortes_data) - 2
    cortes_data.append(["TOTAL", str(total_unidades), f"{area_total:.2f} m²", f"{area_total:.2f} m²"])

    w_corte = [ANCHO * 0.095, ANCHO * 0.075, ANCHO * 0.09, ANCHO * 0.09]
    tabla_cortes = Table(cortes_data, colWidths=w_corte)
    estilo_corte = [
        ("SPAN", (0, 0), (-1, 0)),
        ("BACKGROUND", (0, 0), (-1, 1), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 1), colors.white),
        ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (0, -1), AZUL),
        ("TEXTCOLOR", (0, -1), (0, -1), colors.white),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (3, 2), (3, -2), VERDE),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]
    tabla_cortes.setStyle(TableStyle(estilo_corte))

    # ── TABLA DESPERDICIO ────────────────────────────────────────────────────
    desperdicio_t = Table(
        [
            ["DESPERDICIO", "", ""],
            ["Longitud", "Unidades", "m²"],
            ["0 mm", "0", "0.00"],
            ["0 mm", "0", "0.00"],
            ["TOTAL", "0", "0.00"],
        ],
        colWidths=[ANCHO * 0.083, ANCHO * 0.06, ANCHO * 0.06],
    )
    desperdicio_t.setStyle(TableStyle([
        ("SPAN", (0, 0), (-1, 0)),
        ("BACKGROUND", (0, 0), (-1, 1), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 1), colors.white),
        ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (0, -1), AZUL),
        ("TEXTCOLOR", (0, -1), (0, -1), colors.white),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    # ── TABLA DISTRIBUCIÓN DE PANELES (incluye columna Corte 2) ──────────────
    LARGO_STOCK = 12000
    distribucion = [
        ["DISTRIBUCIÓN DE PANELES", "", "", "", ""],
        ["Panel", "Tamaño\n(mm)", "Corte 1\n(mm)", "Corte 2\n(mm)", "Desperdicio\n(mm)"],
    ]
    contador = 1
    for cortes in cortes_por_fila:
        for corte in cortes:
            distribucion.append([
                str(contador), str(LARGO_STOCK), str(corte), "-", str(LARGO_STOCK - corte),
            ])
            contador += 1

    w_dist = [ANCHO * 0.032, ANCHO * 0.052, ANCHO * 0.052, ANCHO * 0.052, ANCHO * 0.062]
    tabla_distribucion = Table(distribucion, colWidths=w_dist)
    tabla_distribucion.setStyle(TableStyle([
        ("SPAN", (0, 0), (-1, 0)),
        ("BACKGROUND", (0, 0), (-1, 1), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 1), colors.white),
        ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
    ]))

    centro = Table(
        [[tabla_cortes, desperdicio_t, tabla_distribucion]],
        colWidths=[ANCHO * 0.35, ANCHO * 0.203, ANCHO * 0.25],
    )
    centro.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(centro)
    elements.append(Spacer(1, 6))

    # ── PARTE INFERIOR ────────────────────────────────────────────────────────
    tabla_log_usuario = info.get("servicio_logistico_tabla", [
        {"Concepto": "SERVICIO LOGÍSTICO", "Tipo": "MINIMULA", "Cantidad": 1.0, "Precio_COP": 0},
        {"Concepto": "", "Tipo": "", "Cantidad": 0.0, "Precio_COP": 0},
    ])

    def _fmt_cop(valor):
        return f"${valor:,.0f}" if valor and valor > 0 else "$0"

    f1_cant = f"{tabla_log_usuario[0]['Cantidad']:,.2f}"
    f1_cop = _fmt_cop(tabla_log_usuario[0]["Precio_COP"])
    f2_cant = f"{tabla_log_usuario[1]['Cantidad']:,.2f}"
    f2_cop = _fmt_cop(tabla_log_usuario[1]["Precio_COP"])

    icono_camion_1 = _icono_camion()
    icono_camion_2 = _icono_camion()

    servicio = Table(
        [
            ["SERVICIO LOGÍSTICO", "", ""],
            [icono_camion_1, "Tipo", str(tabla_log_usuario[0]["Tipo"])],
            ["", "Cantidad", f1_cant],
            ["", "COP $", f1_cop],
            [icono_camion_2, "Tipo", str(tabla_log_usuario[1]["Tipo"])],
            ["", "Cantidad", f2_cant],
            ["", "COP $", f2_cop],
        ],
        colWidths=[ANCHO * 0.09, ANCHO * 0.11, ANCHO * 0.13],
    )
    servicio.setStyle(TableStyle([
        ("SPAN", (0, 0), (-1, 0)),
        ("SPAN", (0, 1), (0, 3)),
        ("SPAN", (0, 4), (0, 6)),
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (1, 1), (1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    icono_tornillo_1 = _icono_tornillo()
    icono_tornillo_2 = _icono_tornillo()
    nombre_texto = _texto_style(size=7.5, bold=True)

    kits = Table(
        [
            ["KITS DE FIJACIÓN", "", "", ""],
            [icono_tornillo_1, Paragraph("Kit de Fijación<br/>Roof", nombre_texto), "Tipo", "-"],
            ["", "", "Cantidad", "-"],
            ["", "", "COP $", "-"],
            [icono_tornillo_2, Paragraph("Kit de Fijación<br/>Wall-Frigo", nombre_texto), "Tipo", "-"],
            ["", "", "Cantidad", "-"],
            ["", "", "COP $", "-"],
        ],
        colWidths=[ANCHO * 0.06, ANCHO * 0.09, ANCHO * 0.07, ANCHO * 0.06],
    )
    kits.setStyle(TableStyle([
        ("SPAN", (0, 0), (-1, 0)),
        ("SPAN", (0, 1), (0, 3)),
        ("SPAN", (1, 1), (1, 3)),
        ("SPAN", (0, 4), (0, 6)),
        ("SPAN", (1, 4), (1, 6)),
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (2, 1), (2, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    costo_logistico_total = sum(
        item["Cantidad"] * item["Precio_COP"] for item in tabla_log_usuario
    )
    total_orden = 4_600_000 + costo_logistico_total

    totales = Table(
        [
            ["TOTALES", ""],
            ["Área Requerida:", f"{area_total:.2f} m²"],
            ["Área Suministrada:", f"{area_total:.2f} m²"],
            ["Desperdicio Total:", "0.00 m²"],
            ["TOTAL ORDEN", ""],
            [Paragraph(f"<b>${total_orden:,.0f}</b>", _total_style()), "COP"],
        ],
        colWidths=[ANCHO * 0.17, ANCHO * 0.17],
        rowHeights=[18, 16, 16, 16, 18, 34],
    )
    totales.setStyle(TableStyle([
        ("SPAN", (0, 0), (1, 0)),
        ("SPAN", (0, 4), (1, 4)),
        ("SPAN", (0, 5), (0, 5)),
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 4), (-1, 4), AZUL),
        ("TEXTCOLOR", (0, 4), (-1, 4), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 4), (-1, 4), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, 3), [colors.white, GRIS_CLARO]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, 3), 8),
        ("FONTSIZE", (1, 5), (1, 5), 9),
    ]))

    inferior = Table(
        [[servicio, kits, totales]],
        colWidths=[ANCHO * 0.33, ANCHO * 0.28, ANCHO * 0.34],
    )
    inferior.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(inferior)
    elements.append(Spacer(1, 6))

    # ── OBSERVACIONES ─────────────────────────────────────────────────────────
    observaciones = Table(
        [["OBSERVACIONES:"], [info.get("observaciones", "")], [""]],
        colWidths=[ANCHO], rowHeights=[16, 20, 20],
    )
    observaciones.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
        ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 4),
    ]))
    elements.append(observaciones)

    doc.build(elements)
    buffer.seek(0)
    return buffer
