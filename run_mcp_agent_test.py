from src.agent_mcp import MCPResumeMatchAgent

resume_text = """
Experienced Data Scientist with strong Python, SQL,
machine learning, pandas, and scikit-learn experience.
"""

ROLE_SKILLS = [
    "python",
    "sql",
    "machine learning",
    "statistics",
    "pandas",
    "numpy"
]

agent = MCPResumeMatchAgent()
result = agent.run(resume_text, ROLE_SKILLS)

print("SCORE:", result["score"])
print("\nSUMMARY:\n")
print(result["summary"])
