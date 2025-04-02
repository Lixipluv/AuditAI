from fastapi import APIRouter, HTTPException
import os
import json

router = APIRouter(tags=["reports"])

# Diretório de armazenamento dos relatórios
REPORTS_DIR = "app/reports"

# Garante que o diretório de relatórios existe
os.makedirs(REPORTS_DIR, exist_ok=True)

@router.get("/latest")
async def get_latest_report():
    """
    Retorna o relatório mais recente gerado pelo Slither.
    Dá prioridade ao relatório formatado, se disponível.
    """
    try:
        # Lista todos os arquivos JSON na pasta de relatórios
        files = sorted(
            [f for f in os.listdir(REPORTS_DIR) if f.endswith(".json")],
            key=lambda x: os.path.getmtime(os.path.join(REPORTS_DIR, x)),
            reverse=True
        )

        if not files:
            raise HTTPException(status_code=404, detail="Nenhum relatório encontrado.")

        # Tenta priorizar o relatório formatado, se existir
        formatted_report_path = os.path.join(REPORTS_DIR, "latest_formatted.json")
        if os.path.exists(formatted_report_path):
            with open(formatted_report_path, "r", encoding="utf-8") as report_file:
                try:
                    report_data = json.load(report_file)
                    return {"filename": "latest_formatted.json", "report": report_data}
                except json.JSONDecodeError:
                    raise HTTPException(status_code=500, detail="Erro ao decodificar JSON formatado.")

        # Caso contrário, usa o mais recente
        latest_report_path = os.path.join(REPORTS_DIR, files[0])
        with open(latest_report_path, "r", encoding="utf-8") as report_file:
            try:
                report_data = json.load(report_file)
                return {"filename": files[0], "report": report_data}
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Erro ao decodificar JSON do relatório mais recente.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar relatório: {str(e)}")
