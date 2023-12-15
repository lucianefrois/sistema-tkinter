from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
import os
import subprocess

class ReportIndividualPDF:
    def create_pdf(self, pdf_filename, cleaned_name, start_date_str, end_date_str, resultados, valor_total):
        # Define o caminho do diretório para salvar o PDF
        dir_reports = "reports"
        if not os.path.exists(dir_reports):
            os.makedirs(dir_reports)

        # Define o nome do arquivo PDF
        pdf_filename = os.path.join(dir_reports, f"Relatório_{cleaned_name}_{start_date_str.replace('/', '_')}_{end_date_str.replace('/', '_')}.pdf")

        # Cria o PDF
        pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Adiciona o título ao PDF
        title_style = ParagraphStyle(
            'Title',
            parent=getSampleStyleSheet()['Title'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.black,
            alignment=1  # Centraliza o texto
        )
        title_text = f"<b>Relatório Individual</b>"
        title = Paragraph(title_text, title_style)

        # Adiciona informações de consulta ao PDF
        info_style = ParagraphStyle(
            'Info',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=12,
            spaceAfter=6,
            textColor=colors.black
        )
        info_text = f"<b>Nome:</b> {cleaned_name}<br/><b>Data de Início:</b> {start_date_str}<br/><b>Data de Fim:</b> {end_date_str}"
        info = Paragraph(info_text, info_style)

        # Adiciona cabeçalhos à tabela
        headings_style = ParagraphStyle(
            'Headings',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=10,
            spaceAfter=3,
            textColor=colors.black,
            alignment=1  # Centraliza o texto
        )
        headings = [Paragraph(str(heading), headings_style) for heading in ["ID", "Data", "Cliente", "Despachante", "Tipo de Veiculo", "Placa", "Valor", "Status Pagamento", "Op. Caixa"]]

        # Adiciona resultados ao PDF
        data_style = ParagraphStyle(
            'Data',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=10,
            spaceAfter=4,
            textColor=colors.black
        )
        data = []
        for row in resultados:
            row_text = [str(value)[:20] for value in row]
            data.append([Paragraph(cell, data_style) for cell in row_text])

        # Adiciona o valor total ao PDF
        total_style = ParagraphStyle(
            'Total',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=12,
            spaceAfter=14,
            textColor=colors.black
        )
        total_text = f"<b>Total R$:</b> {valor_total:.2f}"
        total = Paragraph(total_text, total_style)

        # Constrói a tabela
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.beige),  # Adiciona cor de fundo para a linha de cabeçalho
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table_data = [headings] + data  # Adiciona a linha de cabeçalho à tabela
        table = Table(table_data, style=table_style)

        # Constrói o PDF
        elements = [title, info, table, total]
        pdf.build(elements)

        # Chama a função para imprimir/abrir o relatório (abrir o PDF)
        self.print_and_open_pdf(pdf_filename)

    def print_and_open_pdf(self, pdf_filename):
        try:
            # Use o comando padrão associado ao tipo de arquivo PDF no sistema
            subprocess.Popen([pdf_filename], shell=True)
        except Exception as e:
            print(f"Erro ao abrir o arquivo PDF: {e}")

class GeneralReportsPDF:
    def create_pdf(self, start_date_str, end_date_str, resultados, total_entrada, total_saida, total_value):
        # Define o caminho do diretório para salvar o PDF
        dir_reports = "reports"
        if not os.path.exists(dir_reports):
            os.makedirs(dir_reports)

        # Define o nome do arquivo PDF
        pdf_filename = os.path.join(dir_reports, f"Relatório_Geral_{start_date_str.replace('/', '_')}_{end_date_str.replace('/', '_')}.pdf")

        # Cria o PDF
        pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Adiciona o título ao PDF
        title_style = ParagraphStyle(
            'Title',
            parent=getSampleStyleSheet()['Title'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.black,
            alignment=1  # Centraliza o texto
        )
        title_text = f"<b>Relatório Geral</b>"
        title = Paragraph(title_text, title_style)

        # Adiciona informações de consulta ao PDF
        info_style = ParagraphStyle(
            'Info',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=12,
            spaceAfter=6,
            textColor=colors.black
        )
        info_text = f"<b>Data de Início:</b> {start_date_str}<br/><b>Data de Fim:</b> {end_date_str}"
        info = Paragraph(info_text, info_style)

        # Adiciona cabeçalhos à tabela
        headings_style = ParagraphStyle(
            'Headings',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=10,
            spaceAfter=3,
            textColor=colors.black,
            alignment=1  # Centraliza o texto
        )
        headings = [Paragraph(str(heading), headings_style) for heading in ["ID", "Data Entrada", "Cliente", "Valor Entrada", "Status", "Data Saída", "Descrição", "Valor Saida"]]

        # Adiciona resultados ao PDF
        data_style = ParagraphStyle(
            'Data',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=10,
            spaceAfter=5,
            textColor=colors.black
        )
        data = []
        for row in resultados:
            row_text = [str(value)[:20] for value in row]
            data.append([Paragraph(cell, data_style) for cell in row_text])

        # Adiciona o valor total ao PDF
        total_style = ParagraphStyle(
            'Total R$',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=12,
            spaceAfter=14,
            textColor=colors.black
        )
        total_entrada_text = f"<b>Total entradas R$:</b> {total_entrada:.2f}"
        total_entrada_text = Paragraph(total_entrada_text, total_style)
        total_saida_text = f"<b>Total saidas R$: -</b> {total_saida:.2f}"
        total_saida_text = Paragraph(total_saida_text, total_style)
        total_text = f"<b>Total Líquido R$:</b> {total_value:.2f}"
        total = Paragraph(total_text, total_style)

        # Constrói a tabela
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.beige),  # Adiciona cor de fundo para a linha de cabeçalho
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table_data = [headings] + data  # Adiciona a linha de cabeçalho à tabela
        table = Table(table_data, style=table_style)

        # Constrói o PDF
        elements = [title, info, table, total_entrada_text, total_saida_text, total]
        pdf.build(elements)

        # Chama a função para imprimir/abrir o relatório (abrir o PDF)
        self.print_and_open_pdf(pdf_filename)

    def print_and_open_pdf(self, pdf_filename):
        try:
            # Use o comando padrão associado ao tipo de arquivo PDF no sistema
            subprocess.Popen([pdf_filename], shell=True)
        except Exception as e:
            print(f"Erro ao abrir o arquivo PDF: {e}")