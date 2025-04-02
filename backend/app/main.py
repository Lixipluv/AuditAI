import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.analysis_api import router as analysis_router
from app.api.reports_api import router as reports_router
from app.api.groq_api import router as groq_router
from app.api.chatbot_api import router as chatbot_router
from app.api.dashboard_api import router as dashboard_router
from app.api.generatorpdf_api import router as pdf_router

# Diretórios do projeto
REPORTS_DIR = "app/reports"
PDF_DIR = "app/pdf_reports"
DEFAULT_REPORT = os.path.join(REPORTS_DIR, "latest_formatted.json")
DEFAULT_PDF = os.path.join(PDF_DIR, "latest_report.pdf")

app = FastAPI(title="AuditAI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrando as rotas
app.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])
app.include_router(groq_router, prefix="/groq", tags=["Groq AI"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(pdf_router, prefix="/pdf", tags=["PDF Generator"])

# Servir PDFs diretamente
app.mount("/pdf_reports", StaticFiles(directory=PDF_DIR), name="pdf_reports")

# Criar diretórios se não existirem
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

def create_default_report():
    """Cria um relatório vazio caso não exista."""
    if not os.path.exists(DEFAULT_REPORT):
        with open(DEFAULT_REPORT, "w", encoding="utf-8") as f:
            json.dump({"results": {"detectors": []}}, f, indent=4)
        print(f"✅ Relatório inicial criado: {DEFAULT_REPORT}")

def create_default_pdf():
    """Cria um PDF inicial baseado no último relatório."""
    from app.api.generatorpdf_api import generate_pdf

    if not os.path.exists(DEFAULT_PDF) or not os.path.getsize(DEFAULT_PDF):
        if os.path.exists(DEFAULT_REPORT):
            generate_pdf(DEFAULT_REPORT, DEFAULT_PDF)
            print(f"✅ PDF inicial gerado: {DEFAULT_PDF}")
        else:
            print("⚠️ Nenhum relatório disponível para gerar PDF.")

# Executar criação dos arquivos iniciais
create_default_report()
create_default_pdf()

@app.get("/")
def root():
    return {"status": "AuditAI Backend está funcionando corretamente."}
