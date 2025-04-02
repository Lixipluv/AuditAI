import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fpdf import FPDF
from bs4 import BeautifulSoup

router = APIRouter(tags=["PDF Generator"])

PDF_DIR = "app/pdf_reports"
DEFAULT_PDF = os.path.join(PDF_DIR, "latest_report.pdf")
os.makedirs(PDF_DIR, exist_ok=True)

LATEST_JSON = os.path.join("app", "reports", "latest_formatted.json")
GROQ_JSON = os.path.join("app", "reports", "latest_groq_formatted.json")

class ReportData(BaseModel):
    vulnerabilities: list

def sanitize_text(text):
    return text if text else "Unknown"

def generate_pdf(json_report_path: str, output_pdf_path: str):
    if not os.path.exists(json_report_path):
        raise HTTPException(status_code=404, detail="JSON report not found.")

    try:
        with open(json_report_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)

        custom_title = report_data.get("custom_title", "Smart Contract Analysis Report")
        formatted_report = report_data.get("formatted_report")
        results = report_data.get("results", [])

        FONT_PATH = "app/fonts/DejaVuSans.ttf"
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        if os.path.exists(FONT_PATH):
            pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
            pdf.set_font("DejaVu", size=12)
        else:
            pdf.set_font("Arial", size=12)

        pdf.set_font("DejaVu" if os.path.exists(FONT_PATH) else "Arial", "B", 16)
        pdf.cell(200, 10, custom_title, ln=True, align="C")
        pdf.set_font("DejaVu" if os.path.exists(FONT_PATH) else "Arial", size=12)
        pdf.ln(10)

        if formatted_report:
            soup = BeautifulSoup(formatted_report, "html.parser")
            tags = soup.find_all(["h2", "h3", "p", "ul", "li", "strong"])
            if tags:
                for tag in tags:
                    text = sanitize_text(tag.get_text())

                    if tag.name == "h2":
                        pdf.set_font("DejaVu" if os.path.exists(FONT_PATH) else "Arial", "B", 14)
                        pdf.cell(0, 10, text, ln=True)
                    elif tag.name == "h3":
                        pdf.set_font("DejaVu" if os.path.exists(FONT_PATH) else "Arial", "B", 12)
                        pdf.cell(0, 8, text, ln=True)
                    elif tag.name == "p":
                        pdf.set_font("DejaVu" if os.path.exists(FONT_PATH) else "Arial", size=11)
                        pdf.multi_cell(0, 8, text)
                        pdf.ln(1)
                    elif tag.name == "li":
                        pdf.set_font("DejaVu" if os.path.exists(FONT_PATH) else "Arial", size=11)
                        pdf.cell(5)
                        pdf.cell(0, 8, f"• {text}", ln=True)
                    elif tag.name == "strong":
                        pdf.set_font("DejaVu" if os.path.exists(FONT_PATH) else "Arial", "B", 11)
                        pdf.cell(0, 8, text, ln=True)
            else:
                pdf.multi_cell(0, 10, sanitize_text(formatted_report))

        elif results:
            for detector in results:
                check = sanitize_text(detector.get("check"))
                description = sanitize_text(detector.get("description"))
                pdf.set_font("DejaVu" if os.path.exists(FONT_PATH) else "Arial", "B", 12)
                pdf.cell(0, 10, f"{check}", ln=True)
                pdf.set_font("DejaVu" if os.path.exists(FONT_PATH) else "Arial", size=11)
                pdf.multi_cell(0, 8, description, border="B")
                pdf.ln(3)
        else:
            pdf.cell(0, 10, "No vulnerabilities found.", ln=True)

        pdf.output(output_pdf_path)
        print(f"✅ PDF generated successfully: {output_pdf_path}")

    except Exception as e:
        print(f"Error generating PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {e}")

@router.get("/latest")
async def get_latest_pdf():
    if not os.path.exists(DEFAULT_PDF):
        raise HTTPException(status_code=404, detail="No PDF found.")
    return {"pdf_url": f"/pdf_reports/latest_report.pdf"}

@router.post("/generate")
async def generate_pdf_endpoint(report_data: ReportData):
    try:
        temp_path = os.path.join(PDF_DIR, "_temp_data.json")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump({"results": report_data.vulnerabilities}, f, indent=4)
        generate_pdf(temp_path, DEFAULT_PDF)
        return {"pdf_url": f"/pdf_reports/latest_report.pdf"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

@router.post("/regenerate-pdf")
async def regenerate_pdf_endpoint():
    if not os.path.exists(LATEST_JSON):
        raise HTTPException(status_code=404, detail="latest_formatted.json not found.")

    try:
        generate_pdf(LATEST_JSON, DEFAULT_PDF)
        return {"pdf_url": f"/pdf_reports/latest_report.pdf"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to regenerate PDF: {str(e)}")