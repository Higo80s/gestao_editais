import io
import csv
from flask import send_file
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from models import Bolsista, Modalidade, Edital
from utils import calcular_parcelas
from datetime import datetime

def gerar_relatorio_excel(mes_referencia_str):
    # mes_referencia_str format: YYYY-MM
    wb = Workbook()
    ws = wb.active
    ws.title = "Pagamento Bolsas"

    # Headers
    headers = [
        "Item", "Edital", "SEI", "CPF", "Nome", "Programa", 
        "Banco", "Agência", "Conta", "Tipo", "Nível", 
        "Valor", "Início Bolsa", "Referência", "Vencimento", 
        "Parcela Atual", "Total Parcelas"
    ]
    ws.append(headers)

    # Reference Date
    ref_date = datetime.strptime(mes_referencia_str + '-01', '%Y-%m-%d').date()

    # Fetch Data
    # In a real scenario, optimize query with joins
    bolsistas = Bolsista.query.filter_by(ativo=True).all()
    
    count = 1
    for b in bolsistas:
        # Get Modality for Value
        mod = Modalidade.query.get(b.modalidade_id)
        edital = Edital.query.get(b.edital_id)
        
        # Calculate Parcel
        parcela = calcular_parcelas(b.data_inicio_bolsa, ref_date, b.data_desligamento)
        
        if parcela > 0 and parcela <= b.meses_duracao:
            row = [
                count,
                edital.numero,
                "N/A", # SEI placeholder (add field if needed)
                b.cpf,
                b.nome,
                b.programa,
                b.banco,
                b.agencia,
                b.conta,
                b.tipo_conta,
                mod.nivel,
                f"R$ {mod.valor_mensal:.2f}",
                b.data_inicio_bolsa.strftime('%d/%m/%Y'),
                mes_referencia_str, # Reference
                "5º dia útil", # Vencimento (placeholder)
                parcela,
                b.meses_duracao
            ]
            ws.append(row)
            count += 1

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

def gerar_relatorio_pdf(mes_referencia_str):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Relatório de Pagamento de Bolsas - {mes_referencia_str}", styles['Title']))

    data = [[
        "Edital", "Nome", "CPF", "Nível", "Valor", "Parcela"
    ]]
    
    ref_date = datetime.strptime(mes_referencia_str + '-01', '%Y-%m-%d').date()
    bolsistas = Bolsista.query.filter_by(ativo=True).all()
    
    for b in bolsistas:
        mod = Modalidade.query.get(b.modalidade_id)
        edital = Edital.query.get(b.edital_id)
        parcela = calcular_parcelas(b.data_inicio_bolsa, ref_date)
        
        if parcela > 0 and parcela <= b.meses_duracao:
            data.append([
                edital.numero,
                b.nome,
                b.cpf,
                mod.nivel,
                f"{mod.valor_mensal:.2f}",
                f"{parcela}/{b.meses_duracao}"
            ])

    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return buffer
