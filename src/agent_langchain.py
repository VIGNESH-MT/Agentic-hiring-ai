from langchain.agents import Tool, initialize_agent


def build_skill_agent(matcher):
    tools = [
        Tool(
            name="extract_resume_skills",
            func=matcher.extract_resume_skills,
            description="Extract skills from resume text"
        ),
        Tool(
            name="match_to_role",
            func=matcher.match_to_role,
            description="Match resume skills to target role"
        )
    ]

    agent = initialize_agent(
        tools=tools,
        llm=None,
        agent="zero-shot-react-description",
        verbose=True
    )

    return agent
