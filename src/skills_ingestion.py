from pathlib import Path
import pandas as pd
from typing import Set

from src.skills_normalizer import normalize_skill


# ---------------------------------------------------
# Load resume-derived skills
# ---------------------------------------------------
def load_resume_skills(skills_catalog_path: Path) -> Set[str]:
    df = pd.read_parquet(skills_catalog_path)
    return set(df["skill"].astype(str).str.lower().str.strip())


# ---------------------------------------------------
# Load skills taxonomy dataset (ROBUST)
# ---------------------------------------------------
def load_taxonomy_skills(csv_path: Path) -> Set[str]:
    df = pd.read_csv(csv_path)

    # Normalize column names: case-insensitive, space/underscore safe
    normalized_cols = {
        col.lower().replace(" ", "").replace("_", ""): col
        for col in df.columns
    }

    # Semantic meanings of "skill"
    candidate_keys = [
        "skill",
        "skills",
        "skillname",
        "allskills",
        "technology",
        "technologies"
    ]

    skill_col = None
    for key in candidate_keys:
        if key in normalized_cols:
            skill_col = normalized_cols[key]
            break

    if skill_col is None:
        raise ValueError(
            f"""
❌ Could not infer skill column from taxonomy dataset.

Available columns:
{df.columns.tolist()}

Expected semantic keys:
{candidate_keys}
"""
        )

    skills = (
        df[skill_col]
        .dropna()
        .astype(str)
        .str.lower()
        .str.strip()
        .apply(normalize_skill)
    )

    return set(skills)


# ---------------------------------------------------
# Load ML/DS job skills dataset
# ---------------------------------------------------
def load_ml_ds_skills(csv_path: Path) -> Set[str]:
    df = pd.read_csv(csv_path)

    # Normalize column names
    normalized_cols = {
        col.lower().replace(" ", "").replace("_", ""): col
        for col in df.columns
    }

    # Typical ML/DS skill columns
    candidate_keys = ["skills", "jobskills", "requiredskills"]

    skills_col = None
    for key in candidate_keys:
        if key in normalized_cols:
            skills_col = normalized_cols[key]
            break

    if skills_col is None:
        raise ValueError(
            f"""
❌ Could not infer skills column from ML/DS dataset.

Available columns:
{df.columns.tolist()}
"""
        )

    skills = (
        df[skills_col]
        .dropna()
        .astype(str)
        .str.lower()
        .str.split(",")
        .explode()
        .str.strip()
        .apply(normalize_skill)
    )

    return set(skills)


# ---------------------------------------------------
# Build unified skills catalog
# ---------------------------------------------------
def build_unified_skills_catalog(
    resume_skills: Set[str],
    taxonomy_skills: Set[str],
    ml_ds_skills: Set[str]
) -> pd.DataFrame:

    unified = sorted(resume_skills | taxonomy_skills | ml_ds_skills)

    return pd.DataFrame({
        "skill": unified,
        "source": "unified_catalog"
    })
