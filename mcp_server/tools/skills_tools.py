from mcp_server.schemas import (
    SkillSearchRequest,
    SkillSearchResponse
)
import pandas as pd


def search_skills_tool(
    req: SkillSearchRequest
) -> SkillSearchResponse:
    try:
        df = pd.read_parquet(
            "data/processed/skills_catalog.parquet"
        )

        results = (
            df["skill"]
            .astype(str)
            .str.lower()
            .str.contains(req.query.lower())
        )

        skills = df.loc[results, "skill"].head(req.top_k).tolist()

        return SkillSearchResponse(skills=skills)

    except Exception as e:
        raise RuntimeError(f"Skill search failed: {e}")
