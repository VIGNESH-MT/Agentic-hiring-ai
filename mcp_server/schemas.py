from pydantic import BaseModel
from typing import List, Literal


class ExtractSkillsRequest(BaseModel):
    resume_text: str


class SkillEvidence(BaseModel):
    skill: str
    confidence: float
    method: Literal["exact", "fuzzy", "semantic"]
    evidence_snippet: str


class ExtractSkillsResponse(BaseModel):
    skills: List[SkillEvidence]


class SkillSearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SkillSearchResponse(BaseModel):
    skills: List[str]


class MatchScoreRequest(BaseModel):
    resume_skills: List[str]
    role_skills: List[str]


class MatchScoreResponse(BaseModel):
    score: float
    matched_skills: List[str]
    missing_skills: List[str]
