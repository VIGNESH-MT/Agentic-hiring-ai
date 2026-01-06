import pandas as pd
import pytest


def build_comparison_df(rows):
    """
    Extracted logic from app.py for unit testing.
    This mirrors the multi-role comparison guard logic.
    """
    df_compare = pd.DataFrame(rows)

    if df_compare.empty:
        return "EMPTY"

    if "Match %" not in df_compare.columns:
        raise ValueError("Missing Match % column")

    df_compare = df_compare.sort_values("Match %", ascending=False)
    return df_compare


def test_empty_roles_does_not_crash():
    """
    Edge case:
    - User clears all roles
    - rows = []
    - App should NOT crash
    """
    rows = []

    result = build_comparison_df(rows)

    assert result == "EMPTY"


def test_valid_roles_sorting():
    """
    Normal case:
    - Roles exist
    - DataFrame sorts correctly
    """
    rows = [
        {"Role": "Data Scientist", "Match %": 70, "Matched Skills": 7, "Total Required": 10},
        {"Role": "ML Engineer", "Match %": 85, "Matched Skills": 8, "Total Required": 9},
    ]

    df = build_comparison_df(rows)

    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["Role"] == "ML Engineer"
    assert df.iloc[0]["Match %"] == 85


def test_missing_match_percent_column():
    """
    Defensive test:
    - Schema changes accidentally
    - Missing 'Match %'
    """
    rows = [
        {"Role": "Data Scientist", "Score": 70}
    ]

    with pytest.raises(ValueError):
        build_comparison_df(rows)
