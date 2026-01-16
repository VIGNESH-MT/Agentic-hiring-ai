# src/agents/langchain_tools/skills_tools.py

from typing import Dict
from pathlib import Path
from langchain.tools import tool
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

_embeddings = None
_vector_store = None


def _load_vector_store() -> FAISS:
    global _embeddings, _vector_store

    if _vector_store:
        return _vector_store

    import pandas as pd
    skills_path = Path("data/processed/skills_catalog.parquet")
    df = pd.read_parquet(skills_path)
    skills = df["skill"].astype(str).str.lower().tolist()

    _embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    _vector_store = FAISS.from_texts(skills, _embeddings)
    return _vector_store


@tool("search_skills")
def search_skills(query: str, top_k: int = 5) -> Dict:
    store = _load_vector_store()
    results = store.similarity_search_with_score(query, k=top_k)

    return {
        "query": query,
        "results": [
            {"skill": d.page_content, "score": round(float(s), 4)}
            for d, s in results
        ],
    }
