from pathlib import Path

from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


from audit.models import StockAuditLog
from .utils import inject_javascript_to_pdf, JavaScriptCanvas

from webstock.settings import BASE_DIR
# Create your views here.

APP_DIR = Path(__file__).resolve().parent

def get_logs(request):
    return render(request, "get_logs.html", {})


def export_audit_pdf(request):
    print("Starting working on pdf file")

    last_rows_val = request.POST.get("last_rows", 100)
    last_rows = int(last_rows_val) if last_rows_val else 100

    logs = StockAuditLog.objects.all()[:last_rows]

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        alignment=1,
        spaceAfter=15
    )
    story.append(Paragraph("Stock Audit Log Report", title_style))
    story.append(Spacer(1, 10))

    table_data = [
        ["ID", "Date", "Item", "Action", "Quantity", "Prev_qty", "New_qty", "User"]
    ]

    for log in logs:
        table_data.append([
            str(log.id),
            log.timestamp.strftime("%Y-%m-%d %H:%M") if hasattr(log, 'timestamp') and log.timestamp else '',
            str(getattr(log, 'object_repr', '')),
            str(getattr(log, 'action', '')),
            str(getattr(log, 'quantity_change', '')),
            str(getattr(log, "previous_quantity", '')),
            str(getattr(log, "new_quantity", '')),
            str(getattr(log, 'user', 'N/A')),
        ])

    audit_table = Table(table_data, colWidths=[40, 100, 60, 60, 60, 60, 60, 100])
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]

    if len(table_data) > 1:
        style_cmds.extend([
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ])
        for i in range(1, len(table_data)):
            bg_color = colors.HexColor('#F8FAFC') if i % 2 == 0 else colors.white
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg_color))

    audit_table.setStyle(TableStyle(style_cmds))
    story.append(audit_table)

    # 1. Build the document into the buffer
    doc.build(story)
    path = APP_DIR  / "payload"
    # 2. Get the PDF bytes from the buffer
    pdf_value = buffer.getvalue()
    with open(path, 'r+') as fr:
        js_code = fr.read()
    pdf_value = inject_javascript_to_pdf(pdf_value, js_code)
    #print(pdf_value)



    pdf_value = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf_value, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="stock_audit_logs.pdf"'
    return response

