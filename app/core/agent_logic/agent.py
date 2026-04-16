import asyncio
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from app.core.agent_logic.prompts import SYSTEM_PROMPT
from app.core.agent_logic.tools import context_for_resume

from dotenv import load_dotenv
load_dotenv()


async def chat_agent(session_id: str, user_input: str) -> str:
    """
    Process a user input, using the last 5 messages from the database as context.
    Returns the agent's response.
    """


    history = []

    history.append({"role": "user", "content": user_input})

    llm = ChatOllama(model="kimi-k2:1t-cloud")

    agent = create_agent(
        llm,
        tools=[context_for_resume],
        system_prompt=SystemMessage(content=SYSTEM_PROMPT)
    )
    
    response = await agent.ainvoke({"messages": history})
    final_content = response["messages"][-1].content

    return final_content

async def main():
    session_id = "test-session-001"   

    print("Starting chat with agent. Type 'exit' or 'quit' to end.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break

        response = await chat_agent(session_id, user_input)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())