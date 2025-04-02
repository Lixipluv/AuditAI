from pydantic import BaseModel
from typing import Any, Dict, Optional


class AnalysisResponse(BaseModel):
    analysis: Dict[str, Any]
    message: str


class Vulnerability(BaseModel):
    check: str
    description: str
    impact: Optional[str] = None
    confidence: Optional[str] = None
    function: Optional[str] = None
    line: Optional[str] = None
