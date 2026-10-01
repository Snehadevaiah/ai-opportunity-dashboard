from pydantic import BaseModel
from typing import Optional, List


class Company(BaseModel):
    name: str
    website: str
    industry: Optional[str] = None
    description: Optional[str] = None
    score: Optional[int] = None
    reason: Optional[str] = None
    priority: Optional[str] = None


class CompanyAnalysis(BaseModel):
    company_name: str
    summary: str
    signals: List[str] = []
    score: int = 0
    score_reason: str = ""
    priority: str = ""
    recommended_persona: str = ""
    persona_reason: str = ""
    recommended_action: str = ""
    uncertainty: str = ""