from mcp_server.schemas import (
    ExtractSkillsRequest,
    ExtractSkillsResponse
)
from src.matcher import SkillMatcher
from src.indexer import SkillIndexer
import pandas as pd


def extract_skills_tool(
    req: ExtractSkillsRequest
) -> ExtractSkillsResponse:
    try:
        skills_df = pd.read_parquet(
            "data/processed/skills_catalog.parquet"
        )
        skills = skills_df["skill"].tolist()

        indexer = SkillIndexer(skills)
        matcher = SkillMatcher(skills, indexer)

        extracted = matcher.extract_resume_skills(req.resume_text)

        return ExtractSkillsResponse(skills=extracted)

    except Exception as e:
        raise RuntimeError(f"Skill extraction failed: {e}")
