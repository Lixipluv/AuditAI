import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq

# Diretório para armazenar os relatórios gerados
REPORTS_DIR = "app/reports"
PDF_DIR = "app/pdf_reports"
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# Caminho do relatório gerado
FORMATTED_REPORT_PATH = os.path.join(REPORTS_DIR, "latest_formatted.json")

# Carregar chave da API Groq
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY não está definido. Configure no .env ou nas variáveis de ambiente.")

# Criar cliente Groq
try:
    client = Groq(api_key=api_key)
    print("✅ Cliente Groq inicializado com sucesso.")
except Exception as e:
    raise RuntimeError(f"❌ Erro ao inicializar o cliente Groq: {e}")

# Configuração do roteador API
router = APIRouter(tags=["Groq AI"])

# Modelo para a solicitação da API
class GroqRequest(BaseModel):
    text: str
    language: str = "pt"
    user_level: str = "médio"
    author: str = "Desconhecido"

async def query_groq_api(request: GroqRequest):
    """
    Reformula um relatório técnico, tornando-o mais legível e formatado corretamente.
    - `text`: Conteúdo do relatório técnico.
    - `language`: Idioma do texto gerado.
    - `user_level`: Nível do usuário ("iniciante", "médio", "avançado").
    - `author`: Nome do autor do relatório.

    Retorna:
    - Texto reformulado em formato estruturado.
    """

    print(f"📤 Enviando relatório para IA... (Primeiros 100 caracteres: {request.text[:100]}...)")

    try:
        # Definição do prompt estruturado
        prompt = f"""
        You are an expert in smart contract security. 
        Please respond concisely to the following question or text. 
        Focus on essential details. If the user requests more detail, you may elaborate.

        The user-level is {request.user_level}, in {request.language}.

        Report Author: {request.author}.
        Report Content:
        {request.text}

        🔍 **Conteúdo do relatório:**
        {request.text}
        """

        # Chamada para a API Groq
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )

        # Verificar resposta
        if chat_completion.choices:
            formatted_response = chat_completion.choices[0].message.content
            print("✅ Resumo gerado com sucesso.")

            # Salvar o relatório formatado como JSON
            save_formatted_report(formatted_response)

            return formatted_response

        print("❌ Nenhuma resposta útil foi retornada pela IA.")
        return "<p>A IA não gerou um resumo válido.</p>"

    except Exception as e:
        print(f"❌ Erro ao chamar a API Groq: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao consultar a IA: {str(e)}")


def save_formatted_report(formatted_text):
    """
    Salva o relatório formatado como um JSON no diretório apropriado.
    """
    try:
        report_data = {"formatted_report": formatted_text}

        with open(FORMATTED_REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4)

        print(f"📂 Relatório formatado salvo em: {FORMATTED_REPORT_PATH}")

    except Exception as e:
        print(f"❌ Erro ao salvar o relatório formatado: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o relatório: {str(e)}")


@router.post("/analyze/")
async def analyze_report(request: GroqRequest):
    """
    Rota que recebe um relatório técnico e retorna uma versão reformulada pela IA da Groq.
    Além de gerar o relatório formatado, também inicia a geração do PDF.
    """
    try:
        result = await query_groq_api(request)

        # Gera automaticamente o PDF após salvar o relatório formatado
        generate_pdf_from_report()

        return {"summary": result}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")


def generate_pdf_from_report():
    """
    Chama a API interna de geração de PDF para converter o relatório formatado.
    """
    from app.api.generatorpdf_api import generate_pdf

    try:
        generate_pdf(FORMATTED_REPORT_PATH)
        print("✅ PDF gerado com sucesso após atualização do relatório.")
    except Exception as e:
        print(f"❌ Erro ao gerar PDF após atualização do relatório: {e}")
