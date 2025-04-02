import os
import json
import re
from typing import Dict
from datetime import datetime

LATEST_JSON = os.path.join("app", "reports", "latest_formatted.json")
HISTORY_DIR = os.path.join("app", "reports", "history")
os.makedirs(HISTORY_DIR, exist_ok=True)

def apply_instructions_to_report(instructions: str) -> Dict:
    """
    Aplica instruções da IA ao relatório salvo em latest_formatted.json.

    Suporta:
    - alterar título para "..."
    - adicionar seção "..."
    - substituir "A" por "B"
    - sobrescrever o conteúdo com HTML direto (quando for um relatório completo)
    """

    if not os.path.exists(LATEST_JSON):
        raise FileNotFoundError("❌ Arquivo 'latest_formatted.json' não encontrado.")

    with open(LATEST_JSON, "r", encoding="utf-8") as f:
        report_data = json.load(f)

    # Se estiver no formato de lista, converte para estrutura válida
    if isinstance(report_data, list):
        report_data = {
            "custom_title": "AuditAI Report",
            "formatted_report": "<h2>Relatório Inicial</h2><p>Importado de análise anterior.</p>",
            "results": {"detectors": report_data}
        }
        with open(LATEST_JSON, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)

    if not isinstance(report_data, dict):
        raise ValueError("❌ O conteúdo de 'latest_formatted.json' não é um objeto JSON válido.")

    formatted_html = report_data.get("formatted_report", "")
    if not formatted_html.strip():
        report_data["formatted_report"] = "<p>Conteúdo inicial vazio.</p>"

    # Backup antes de modificar
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(HISTORY_DIR, f"formatted_{timestamp}.json")
    with open(backup_path, "w", encoding="utf-8") as backup:
        json.dump(report_data, backup, indent=4, ensure_ascii=False)

    updated = False

    # 🧠 Sobrescrever com HTML direto
    if instructions.strip().startswith("<h") or "<html" in instructions:
        report_data["formatted_report"] = instructions.strip()
        updated = True

    # 🧠 Alterar título
    match_title = re.search(r"alterar\s+t[ií]tulo\s+para\s+\"(.*?)\"", instructions, re.IGNORECASE)
    if match_title:
        report_data["custom_title"] = match_title.group(1).strip()
        updated = True

    # 🧠 Adicionar seção
    match_section = re.search(r"adicionar\s+se[cç][aã]o\s+\"(.*?)\"", instructions, re.IGNORECASE | re.DOTALL)
    if match_section:
        section_text = match_section.group(1).strip()
        report_data["formatted_report"] += f"\n<h2>Seção Adicional</h2>\n<p>{section_text}</p>"
        updated = True

    # 🧠 Substituir múltiplos
    substitutions = re.findall(r"substituir\s+\"(.*?)\"\s+por\s+\"(.*?)\"", instructions, re.IGNORECASE)
    for old, new in substitutions:
        report_data["formatted_report"] = re.sub(re.escape(old), new, report_data["formatted_report"], flags=re.IGNORECASE)
        updated = True

    if not updated:
        print("⚠️ Nenhuma modificação foi aplicada.")
        return report_data

    # Salvar alterações
    with open(LATEST_JSON, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4, ensure_ascii=False)

    return report_data
