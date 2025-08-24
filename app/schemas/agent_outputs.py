from pydantic import BaseModel, ValidationError, Field
from typing import List, Dict, Any

class AnalysisStructured(BaseModel):
    points: List[str]

class CritiqueStructured(BaseModel):
    issues: List[str]

class AgentOutput(BaseModel):
    final: str
    draft: str
    critique: str
    analysis_structured: AnalysisStructured
    critique_structured: CritiqueStructured
    rag_citations: List[str]
    web_citations: List[str]
    analysis_warnings: List[str]
    critique_warnings: List[str]
