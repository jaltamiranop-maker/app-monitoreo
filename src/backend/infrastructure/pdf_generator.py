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


AZUL = colors.HexColor("#003B8E")


def _titulo_style():
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        "titulo",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        textColor=colors.white,
        fontSize=18,
        leading=22,
    )


def _normal_center():
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        "normal_center",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=9,
    )


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
        topMargin=15, leftMargin=15, rightMargin=15, bottomMargin=15,
    )

    titulo_style = _titulo_style()
    elements = []

    # ── HEADER ───────────────────────────────────────────────────────────────
    header = Table(
        [[
            Paragraph("<b>ORDEN DE PEDIDO</b>", titulo_style),
            Paragraph(f"<b>N° ORDEN<br/>{info.get('n_orden', '0000')}</b>", titulo_style),
        ]],
        colWidths=[420, 110],
    )
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 1, colors.white),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
    ]))
    elements.append(header)
    elements.append(Spacer(1, 10))

    # ── DATOS CLIENTE ─────────────────────────────────────────────────────────
    datos_cliente = [
        ["Cliente:", info.get("cliente", ""), "Proyecto:", ""],
        ["Nombre Contacto:", info.get("contacto", ""), "N° Teléfono Obra:", info.get("telefono", "")],
        ["Teléfono Contacto:", info.get("telefono", ""), "E-Mail Contacto:", info.get("correo", "")],
        ["Tipo de Destino:", info.get("tipo_destino", ""), "Tipo de Obra:", info.get("mercado", "")],
        ["Ubicación Proyecto:", info.get("ciudad", ""), "Tipo de Proyecto:", "NUEVA CONSTRUCCIÓN"],
        ["Dirección Entrega:", info.get("direccion", ""), "Transporte a Cargo de:", info.get("transporte", "")],
        ["Fecha compromiso entrega en Planta:", info.get("f_entrega", ""), "", ""],
    ]

    tabla_cliente = Table(datos_cliente, colWidths=[110, 160, 110, 150])
    tabla_cliente.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), AZUL),
        ("BACKGROUND", (2, 0), (2, 5), AZUL),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("TEXTCOLOR", (2, 0), (2, 5), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTNAME", (3, 0), (3, -1), "Helvetica"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("SPAN", (1, 6), (3, 6)),
    ]))
    elements.append(tabla_cliente)
    elements.append(Spacer(1, 15))

    # ── CÁLCULOS GENERALES ────────────────────────────────────────────────────
    area_total = 0
    total_unidades = 0
    for fila in data_tabla:
        cortes = [int(x.strip()) for x in str(fila["Cortes"]).split(",")]
        area_total += sum(cortes) / 1000
        total_unidades += len(cortes)

    # ── RESUMEN SUPERIOR ──────────────────────────────────────────────────────
    resumen_superior = Table(
        [[
            Paragraph("<b>TIPO DE PRODUCTO</b><br/><br/>PANEL", titulo_style),
            Table(
                [
                    ["Longitud\n(mm)", "Unidades", "Área\n(m²)"],
                    ["9.000", str(total_unidades), f"{area_total:.2f}"],
                ],
                colWidths=[90, 90, 90],
            ),
            Table(
                [
                    ["RESUMEN", ""],
                    ["Área Requerida:", f"{area_total:.2f} m²"],
                    ["Área Suministrada:", f"{area_total:.2f} m²"],
                    ["Desperdicio Total:", "0.00 m²"],
                ],
                colWidths=[120, 120],
            ),
        ]],
        colWidths=[120, 280, 240],
    )
    resumen_superior.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(resumen_superior)
    elements.append(Spacer(1, 15))

    # ── TABLAS CENTRALES ──────────────────────────────────────────────────────
    cortes_data = [["Corte", "Unidades", "Requerido", "Suministrado"]]
    for fila in data_tabla:
        for corte in [int(x.strip()) for x in str(fila["Cortes"]).split(",")]:
            cortes_data.append([
                f"{corte} mm", "1",
                f"{corte / 1000:.2f} m²", f"{corte / 1000:.2f} m²",
            ])
    cortes_data.append(["TOTAL", str(total_unidades), f"{area_total:.2f} m²", f"{area_total:.2f} m²"])

    tabla_cortes = Table(cortes_data, colWidths=[70, 60, 90, 90])
    tabla_cortes.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("BACKGROUND", (0, -1), (0, -1), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("TEXTCOLOR", (0, -1), (0, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    desperdicio_t = Table(
        [["Longitud", "Unidades", "m²"],
         ["0 mm", "0", "0.00"], ["0 mm", "0", "0.00"], ["TOTAL", "0", "0.00"]],
        colWidths=[90, 70, 70],
    )
    desperdicio_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("BACKGROUND", (0, -1), (0, -1), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("TEXTCOLOR", (0, -1), (0, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    distribucion = [["Panel", "Tamaño", "Corte 1", "Desperdicio"]]
    contador = 1
    for fila in data_tabla:
        for corte in [int(x.strip()) for x in str(fila["Cortes"]).split(",")]:
            distribucion.append([str(contador), "12000", str(corte), str(12000 - corte)])
            contador += 1

    tabla_distribucion = Table(distribucion, colWidths=[45, 70, 70, 80])
    tabla_distribucion.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    centro = Table([[tabla_cortes, desperdicio_t, tabla_distribucion]], colWidths=[240, 180, 265])
    elements.append(centro)
    elements.append(Spacer(1, 20))

    # ── PARTE INFERIOR ────────────────────────────────────────────────────────
    tabla_log_usuario = info.get("servicio_logistico_tabla", [
        {"Concepto": "SERVICIO LOGÍSTICO", "Tipo": "MINIMULA", "Cantidad": 1.0, "Precio_COP": 0},
        {"Concepto": "", "Tipo": "", "Cantidad": 0.0, "Precio_COP": 0},
    ])

    f1_cant = f"{tabla_log_usuario[0]['Cantidad']:,.2f}"
    f1_cop = f"${tabla_log_usuario[0]['Precio_COP']:,.0f}" if tabla_log_usuario[0]["Precio_COP"] > 0 else "$0"
    f2_cant = f"{tabla_log_usuario[1]['Cantidad']:,.2f}"
    f2_cop = f"${tabla_log_usuario[1]['Precio_COP']:,.0f}" if tabla_log_usuario[1]["Precio_COP"] > 0 else "$0"

    servicio = Table(
        [
            ["SERVICIO LOGÍSTICO", ""],
            ["Tipo", str(tabla_log_usuario[0]["Tipo"])],
            ["Cantidad", f1_cant],
            ["COP $", f1_cop],
            ["", ""],
            ["Tipo", str(tabla_log_usuario[1]["Tipo"])],
            ["Cantidad", f2_cant],
            ["COP $", f2_cop],
        ],
        colWidths=[120, 120],
    )
    servicio.setStyle(TableStyle([
        ("SPAN", (0, 0), (1, 0)),
        ("SPAN", (0, 4), (1, 4)),
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    costo_logistico_total = sum(
        item["Cantidad"] * item["Precio_COP"] for item in tabla_log_usuario
    )
    total_orden = 4_600_000 + costo_logistico_total

    kits = Table(
        [["KITS DE FIJACIÓN", ""], ["Tipo", ""], ["Cantidad", ""], ["COP $", ""],
         ["", ""], ["Tipo", ""], ["Cantidad", ""], ["COP $", ""]],
        colWidths=[120, 120],
    )

    totales = Table(
        [
            ["TOTALES", ""],
            ["Área Requerida:", f"{area_total:.2f} m²"],
            ["Área Suministrada:", f"{area_total:.2f} m²"],
            ["Desperdicio Total:", "0.00 m²"],
            ["TOTAL ORDEN", ""],
            [f"${total_orden:,.0f}", "COP"],
        ],
        colWidths=[140, 120],
    )

    _base_style = [
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]
    for t in [kits, totales]:
        t.setStyle(TableStyle(_base_style))

    inferior = Table([[servicio, kits, totales]], colWidths=[240, 240, 260])
    elements.append(inferior)
    elements.append(Spacer(1, 20))

    # ── OBSERVACIONES ─────────────────────────────────────────────────────────
    observaciones = Table([["OBSERVACIONES:"], [""], [""]], colWidths=[740])
    observaciones.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ROWHEIGHT", (1, 1), (-1, -1), 40),
    ]))
    elements.append(observaciones)

    doc.build(elements)
    buffer.seek(0)
    return buffer
