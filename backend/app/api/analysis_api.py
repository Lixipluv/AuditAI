import os
import json
import re
import shutil
import subprocess
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, BackgroundTasks, Request
from app.api.generatorpdf_api import generate_pdf
from app.api.dashboard_api import broadcast_dashboard_update
from app.api.groq_api import query_groq_api, GroqRequest  # Não esqueça essa importação!

# Diretórios base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "..", "contracts")
REPORTS_DIR = os.path.join(BASE_DIR, "..", "reports")
PDF_DIR = os.path.join(BASE_DIR, "..", "pdf_reports")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

router = APIRouter(tags=["analysis"])

@router.post("/slither")
async def slither_analysis(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    solc_version: str = Form("auto")
):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        original_report_path = os.path.join(REPORTS_DIR, f"{file.filename}_original.json")
        formatted_report_path = os.path.join(REPORTS_DIR, f"{file.filename}_formatted.json")
        pdf_report_path = os.path.join(PDF_DIR, f"{file.filename}.pdf")

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if solc_version == "auto":
            with open(file_location, "r", encoding="utf-8") as f:
                content = f.read()
            match = re.search(r"pragma solidity\s+([\^~]?\d+\.\d+\.\d+);", content)
            solc_version = match.group(1).lstrip("^~") if match else "0.8.23"

        docker_contract_path = f"/share/contracts/{file.filename}"
        report_path = f"/share/reports/{file.filename}.json"

        subprocess.run(["docker", "cp", file_location, f"smart_read_analyzer:{docker_contract_path}"], check=True)
        subprocess.run(["docker", "exec", "smart_read_analyzer", "rm", "-f", report_path], check=True)

        result = subprocess.run(
            ["docker", "exec", "smart_read_analyzer", "bash", "-c",
             f"solc-select install {solc_version} || true && solc-select use {solc_version} && slither {docker_contract_path} --json {report_path}"],
            capture_output=True, text=True
        )

        if result.returncode != 0 and "Error" in result.stderr:
            raise HTTPException(status_code=500, detail=f"Compilation or Slither error: {result.stderr}")

        subprocess.run(["docker", "cp", f"smart_read_analyzer:{report_path}", original_report_path], check=True)

        with open(original_report_path, "r", encoding="utf-8") as report_file:
            report_data = json.load(report_file)

        structured_data = []
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "unknown": 0}

        for detector in report_data.get("results", {}).get("detectors", []):
            impact = detector.get("impact", "unknown").lower()
            if impact not in severity_counts:
                impact = "unknown"
            severity_counts[impact] += 1

            structured_data.append({
                "check": detector.get("check", "Unknown"),
                "description": detector.get("description", ""),
                "impact": detector.get("impact", "Unknown"),
                "confidence": detector.get("confidence", "Unknown"),
            })

        latest_json_path = os.path.join(REPORTS_DIR, "latest_formatted.json")
        with open(latest_json_path, "w", encoding="utf-8") as latest_file:
            json.dump(structured_data, latest_file, indent=4, ensure_ascii=False)

        # Groq AI para o PDF
        raw_text = "\n".join([
            f"[{item['impact']}] {item['check']} - {item['description']}"
            for item in structured_data
        ])

        groq_request = GroqRequest(text=raw_text, language="pt", user_level="médio", author="Automático")
        formatted_text = await query_groq_api(groq_request)

        groq_formatted_report = {
            "custom_title": "Relatório de Segurança - AuditAI",
            "formatted_report": formatted_text,
            "results": structured_data
        }

        groq_json_path = os.path.join(REPORTS_DIR, "latest_groq_formatted.json")
        with open(groq_json_path, "w", encoding="utf-8") as formatted_file:
            json.dump(groq_formatted_report, formatted_file, indent=4, ensure_ascii=False)

        # Gera PDF usando Groq
        generate_pdf(groq_json_path, pdf_report_path)
        shutil.copyfile(pdf_report_path, os.path.join(PDF_DIR, "latest_report.pdf"))

        await broadcast_dashboard_update({
            "vulnerabilities": structured_data,
            "severity_counts": severity_counts
        })

        # 🚨 Retorno exato exigido pelo frontend:
        return {
            "filename": file.filename,
            "original_report_path": original_report_path,
            "formatted_report_path": formatted_report_path,
            "pdf_report_path": pdf_report_path,
            "formatted_report": structured_data,  # GARANTA ESSA LINHA!
            "severity_counts": severity_counts,
            "pdf_url": f"/pdf_reports/{file.filename}.pdf"
        }

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Slither execution failed: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/customize-pdf")
async def customize_pdf(request: Request):
    try:
        data = await request.json()

        groq_json_path = os.path.join(REPORTS_DIR, "latest_groq_formatted.json")
        if not os.path.exists(groq_json_path):
            raise HTTPException(status_code=404, detail="latest_groq_formatted.json não encontrado.")

        with open(groq_json_path, "r", encoding="utf-8") as f:
            report = json.load(f)

        # Personalizações específicas para Groq PDF
        if "custom_title" in data:
            report["custom_title"] = data["custom_title"]
        if "auditor_name" in data:
            report["auditor"] = data["auditor_name"]
        if "instructions" in data:
            report["formatted_report"] += f"\n\n{data['instructions']}"

        with open(groq_json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)

        generate_pdf(groq_json_path, os.path.join(PDF_DIR, "latest_report.pdf"))

        return {"message": "Relatório Groq personalizado com sucesso."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
