from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing, Rect, String
from io import BytesIO


def generar_pdf(info, data_tabla):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=20)
    elements = []
    styles = getSampleStyleSheet()
    
    header_table = [[Paragraph(f"<font size=14>ORDEN DE PRODUCCIÓN N° {info['n_orden']}</font>", styles['Title'])]]
    t_header = Table(header_table, colWidths=[150, 350])
    t_header.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    elements.append(t_header)
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#c5a367")))
    elements.append(Spacer(1, 15))

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

    elements.append(Paragraph("<b>GUÍA VISUAL PARA CORTE</b>", styles['Heading3']))

    for fila in data_tabla:
        d = Drawing(500, 50)
        ancho_total = 500
        longitud_panel = fila["Tamaño"]

        d.add(Rect(0, 10, ancho_total, 30, fillColor=colors.lightgrey))

        cortes_lista = [int(x.strip()) for x in str(fila["Cortes"]).split(",")]
        x_actual = 0

        for corte in cortes_lista:
            ancho_corte = (corte / longitud_panel) * ancho_total
            d.add(Rect(x_actual, 10, ancho_corte, 30, fillColor=colors.HexColor("#004a99")))
            d.add(String(x_actual + 2, 15, f"{corte}mm", fontSize=7, fillColor=colors.white))
            x_actual += ancho_corte

        elements.append(Paragraph(f"Panel {fila['Panel']} ({fila['Tamaño']} mm)", styles['Normal']))
        elements.append(d)
        elements.append(Spacer(1, 10))

    doc.build(element)
    buffer.seek(0)
    return buffer