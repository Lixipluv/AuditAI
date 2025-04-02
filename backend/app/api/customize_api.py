from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import json

router = APIRouter(tags=["customize"])

REPORT_PATH = "app/reports/latest_formatted.json"

class InstructionRequest(BaseModel):
    instructions: str

@router.post("/customize")
async def customize_report(request: InstructionRequest):
    try:
        if not os.path.exists(REPORT_PATH):
            raise HTTPException(status_code=404, detail="Report not found.")

        with open(REPORT_PATH, "r", encoding="utf-8") as file:
            report_data = json.load(file)

        # Simulação: Adiciona a instrução como uma entrada extra
        report_data.append({
            "check": "custom-instruction",
            "description": request.instructions,
            "impact": "Custom",
            "confidence": "Custom"
        })

        with open(REPORT_PATH, "w", encoding="utf-8") as file:
            json.dump(report_data, file, indent=4)

        return {"status": "updated", "new_length": len(report_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error customizing report: {str(e)}")
