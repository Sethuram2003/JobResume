import asyncio
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from app.core.agent_logic.prompts import SYSTEM_PROMPT_JSON_EXTRACTOR
from app.core.model import AIResponse

from dotenv import load_dotenv
load_dotenv()


async def json_extractor(content:str) -> AIResponse:
    """
    Extract structured resume data from the agent's response content.
    """

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

    print("Raw agent response content:")
    print(final_content)

    print("\nParsed AIResponse object:")
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