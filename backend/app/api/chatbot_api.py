import os
import json
import shutil
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from groq import Groq
from typing import List
from bs4 import BeautifulSoup
from app.api.generatorpdf_api import generate_pdf
from app.models.services.editor import apply_instructions_to_report
import logging


# Load GROQ API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is not set. Please configure it in your .env or environment variables.")

# Initialize Groq client
try:
    client = Groq(api_key=api_key)
    print("Groq client initialized successfully.")
except Exception as e:
    raise RuntimeError(f"Error initializing Groq client: {e}")

# API router configuration
router = APIRouter(tags=["Chatbot and Reports"])

class GroqRequest(BaseModel):
    text: str
    mode: str  # "chatbot" or "report"
    language: str = "auto"
    user_level: str = "medium"
    author: str = "Unknown"

class VulnerabilityInstruction(BaseModel):
    check: str
    description: str
    impact: str
    confidence: str | None = None

class ChatInstruction(BaseModel):
    user_message: str

@router.post("/analyze/")
async def analyze_report(request: GroqRequest):
    try:
        print(f"Incoming JSON: {request.dict()}")
        contains_code = any(keyword in request.text.lower() for keyword in ["contract", "function", "modifier", "solidity"])

        if request.mode == "chatbot":
            response_text = await query_groq_chatbot(request.text, contains_code, request.language)
        elif request.mode == "report":
            response_text = await query_groq_report(request)
        else:
            raise HTTPException(status_code=400, detail="Invalid mode. Choose 'chatbot' or 'report'.")

        return {"response": response_text}

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def query_groq_chatbot(user_message: str, contains_code: bool, language: str):
    try:
        if contains_code:
            prompt = f"""
            You are an advanced smart contract security analyst. Be precise, technical and brief.
            Analyze the following Solidity code for vulnerabilities.
            Provide risks and clear mitigation strategies.
            Language: {language}

            ```solidity
            {user_message}
            ```
            """
        else:
            prompt = f"""
            You are a senior smart contract auditor.
            Answer the user's question briefly, with clear and accurate technical details only.
            Avoid introductions or pleasantries.
            Language: {language}

            Question:
            {user_message}
            """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )

        if chat_completion.choices:
            return chat_completion.choices[0].message.content
        return "No valid response generated."

    except Exception as e:
        print(f"Error in chatbot mode: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chatbot response: {str(e)}")


async def query_groq_report(request: GroqRequest):
    try:
        prompt = f"""
        You are a top-tier smart contract security expert.
        Rewrite the report below using clear, concise, and technical language.
        Prioritize brevity and accuracy. Avoid introductions or generic commentary.
        Use bullet points and clean formatting when possible.

        Language: {request.language}
        User Level: {request.user_level}
        Author: {request.author}

        Report:
        {request.text}
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )

        if chat_completion.choices:
            content = chat_completion.choices[0].message.content
            try:
                parsed = json.loads(content)
                return {"summary": "Customized content applied.", "instructions": parsed}
            except json.JSONDecodeError:
                return {"summary": content, "instructions": None}

    except Exception as e:
        print(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing report: {str(e)}")


@router.post("/chat/update-report")
async def update_report_via_chat(instruction: ChatInstruction):
    report_path = "app/reports/latest_formatted.json"
    groq_report_path = "app/reports/latest_groq_formatted.json"

    try:
        ia_response = instruction.user_message.strip()

        # Carregar JSON atual existente
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                current_report = json.load(f)
        else:
            current_report = {
                "custom_title": "Report Gerated by AuditAI",
                "formatted_report": "",
                "results": {"detectors": []}
            }

        # Manter o estado original para não perder informações
        original_report = current_report.get("formatted_report", "")

        # Aplicar mudanças feitas pela IA com BeautifulSoup
        soup_new = BeautifulSoup(ia_response, "html.parser")

        # Preservar título
        title_tag = soup_new.find("h2")
        custom_title = title_tag.get_text(strip=True) if title_tag else current_report.get("custom_title", "Relatório Gerado pela IA")
        if title_tag:
            title_tag.decompose()

        # Combinar conteúdo antigo com o novo, ao invés de substituir diretamente
        updated_content = f"{original_report}\n{soup_new.prettify()}"

        current_report.update({
            "custom_title": custom_title,
            "formatted_report": updated_content,
            "updated_at": datetime.now().isoformat()
        })

        # Criar backup do relatório atual antes de sobrescrever
        backup_path = f"app/reports/backups/latest_formatted_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        with open(backup_path, "w", encoding="utf-8") as backup_f:
            json.dump(current_report, backup_f, indent=4, ensure_ascii=False)

        # Salvar relatório atualizado com conteúdo combinado
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(current_report, f, indent=4, ensure_ascii=False)

        # Gerar PDF com relatório atualizado
        generate_pdf(report_path, "app/pdf_reports/latest_report.pdf")

        logging.info(f"Relatório atualizado com sucesso. PDF gerado em: app/pdf_reports/latest_report.pdf")

        return {
            "message": "✅ Relatório atualizado com sucesso, preservando alterações anteriores.",
            "updated_json": current_report,
            "pdf_url": "/pdf_reports/latest_report.pdf"
        }

    except Exception as e:
        logging.exception("Erro ao atualizar relatório via chat.")
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")


