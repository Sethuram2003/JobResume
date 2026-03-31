import asyncio
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from app.core.agent_logic.prompts import SYSTEM_PROMPT_JSON_EXTRACTOR
from app.core.model import AIResponse, ResumeData, PersonalInfo, Education

from dotenv import load_dotenv
load_dotenv()


import json
from pathlib import Path
from pydantic import ValidationError


async def json_extractor(content: str) -> AIResponse:
    """
    Extract structured resume data from the agent's response content,
    but always use hardcoded personal_info and education from data.json.
    """

    data_file = Path("data.json")
    if not data_file.exists():
        raise FileNotFoundError("data.json not found. Please provide the file with personal_info and education.")

    with open(data_file, "r", encoding="utf-8") as f:
        hardcoded_data = json.load(f)

    try:
        hardcoded_personal = PersonalInfo.parse_obj(hardcoded_data["personal_info"])
        hardcoded_education = [Education.parse_obj(edu) for edu in hardcoded_data["education"]]
    except (KeyError, ValidationError) as e:
        raise ValueError(f"Invalid data.json format: {e}")

    history = []
    history.append({"role": "user", "content": content})

    llm = ChatOllama(model="deepseek-v3.1:671b-cloud")
    agent = create_agent(
        llm,
        system_prompt=SystemMessage(content=SYSTEM_PROMPT_JSON_EXTRACTOR)
    )

    response = await agent.ainvoke({"messages": history})
    final_content = response["messages"][-1].content

    result = AIResponse.parse_raw(final_content)

    # if result.resume is None:
    #     result.resume = ResumeData(
    #         personal_info=hardcoded_personal,
    #         education=hardcoded_education,
    #         skills=[],
    #         experience=[],
    #         projects=[]
    #     )
    # else:
    #     result.resume.personal_info = hardcoded_personal
    #     result.resume.education = hardcoded_education

    print("Raw agent response content:")
    print(final_content)
    print("\nParsed AIResponse object (with overrides):")
    print(result)

    return result

async def main():
    session_id = "test-session-001"   

    print("Starting chat with agent. Type 'exit' or 'quit' to end.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break

        response = await json_extractor(user_input)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())