import os
import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
from app.models.services.utils import ensure_directory_exists

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "..", "..", "pdf_reports")
ensure_directory_exists(REPORTS_DIR)


def generate_chart(findings_by_severity):
    labels = list(findings_by_severity.keys())
    values = [len(findings) for findings in findings_by_severity.values()]
    colors = ['#ff4c4c', '#ff944c', '#ffc44c', '#9ccc65', '#90caf9']

    if sum(values) == 0:
        print("⚠️ Nenhuma vulnerabilidade detectada. O gráfico não será gerado.")
        return None

    plt.figure(figsize=(6, 4))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title("Distribuição das Vulnerabilidades", fontsize=14, fontweight="bold")

    chart_path = os.path.join(REPORTS_DIR, "chart.png")
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()
    return chart_path


def generate_report(slither_results, query_groq_api, language="pt", author="Desconhecido", level="médio"):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report_text = f"Smart Report - Relatório de Segurança\n\nData: {timestamp}\n\n"
    report_text += f"Autor: {author}\nNível Técnico: {level}\nIdioma: {language}\n\n"

    findings_by_severity = {}
    for issue in slither_results.get("results", {}).get("detectors", []):
        severity = issue.get("impact", "Indefinido")
        findings_by_severity.setdefault(severity, []).append(issue)

    for severity, findings in findings_by_severity.items():
        report_text += f"\n{severity.upper()} - {len(findings)} vulnerabilidades encontradas\n"
        report_text += "=" * 50 + "\n"
        for f in findings:
            description = f.get("description", "Sem descrição disponível")
            processed_description = query_groq_api(description, language)
            function_name = f.get("function", "Função desconhecida")
            line_number = f.get("line", "Linha desconhecida")
            report_text += f"- Função: {function_name} (Linha {line_number})\n  {processed_description}\n"
        report_text += "\n"

    return report_text, findings_by_severity


def save_report(report_text, findings_by_severity=None, filename="latest_report.pdf", custom_title=None, output_format="pdf"):
    ensure_directory_exists(REPORTS_DIR)

    # Gera gráfico se necessário
    chart_path = generate_chart(findings_by_severity or {}) if findings_by_severity else None
    output_file = os.path.join(REPORTS_DIR, filename)

    if output_format == "pdf":
        save_pdf_report(report_text, output_file, chart_path, custom_title)
    elif output_format == "txt":
        save_txt_report(report_text, output_file)
    elif output_format == "html":
        save_html_report(report_text, output_file, custom_title)
    else:
        raise ValueError("Formato não suportado. Use 'pdf', 'txt' ou 'html'.")

    print(f"✅ Relatório salvo com sucesso em: {output_file}")
    return output_file


def save_pdf_report(report_text, output_file, chart_path=None, custom_title=None):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Título
    pdf.set_fill_color(1, 178, 246)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 16)
    header_title = custom_title or "Smart Report - Relatório de Segurança"
    pdf.cell(200, 15, header_title, ln=True, align="C", fill=True)
    pdf.ln(10)

    # Corpo
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)

    for line in report_text.split("\n"):
        if line.strip():
            if "VULNERABILIDADES" in line or "CONCLUSÃO" in line or line.isupper():
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, line, ln=True)
                pdf.set_font("Arial", size=12)
            else:
                pdf.multi_cell(0, 8, line)
        pdf.ln(1)

    if chart_path and os.path.exists(chart_path):
        pdf.add_page()
        pdf.image(chart_path, x=20, y=pdf.get_y(), w=170)

    pdf.output(output_file)


def save_txt_report(report_text, output_file):
    if not output_file.endswith(".txt"):
        output_file = output_file.replace(".pdf", ".txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_text)


def save_html_report(report_text, output_file, title="Smart Report - Relatório de Segurança"):
    if not output_file.endswith(".html"):
        output_file = output_file.replace(".pdf", ".html")

    html_content = f"""<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 2rem;
            line-height: 1.6;
            background-color: #f9f9f9;
            color: #1e293b;
        }}
        h1 {{
            background-color: #1e90ff;
            color: white;
            padding: 10px;
            border-radius: 6px;
        }}
        pre {{
            background: #f1f5f9;
            padding: 1rem;
            border-radius: 6px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <pre>{report_text}</pre>
</body>
</html>
"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
