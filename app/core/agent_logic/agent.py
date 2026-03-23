import asyncio
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from app.core.mysql_database.mysql_service import get_mysql_service, close_mysql_service
from app.core.agent_logic.prompts import SYSTEM_PROMPT
from app.core.agent_logic.tools import context_for_resume
from app.core.model import AIResponse, ResumeData
import json
import re
from dotenv import load_dotenv
load_dotenv()

def db_messages_to_langchain(messages):
    """Convert list of dicts from DB to LangChain message list."""
    lc_messages = []
    for msg in messages:
        if msg["sender_type"] == "user":
            lc_messages.append({"role": "user", "content": msg["message"]})
        else:
            lc_messages.append({"role": "assistant", "content": msg["message"]})
    return lc_messages

async def chat_agent(session_id: str, user_input: str) -> str:
    """
    Process a user input, using the last 5 messages from the database as context.
    Returns the agent's response.
    """
    manager = get_mysql_service()

    recent_messages = manager.get_session_history(
        session_identifier=session_id,
        limit=50,
        order="desc"
    )
    recent_messages.reverse() 

    history = db_messages_to_langchain(recent_messages)

    history.append({"role": "user", "content": user_input})

    llm = ChatOllama(model="deepseek-v3.1:671b-cloud")

    agent = create_agent(
        llm,
        tools=[context_for_resume],
        system_prompt=SYSTEM_PROMPT,
        response_format=AIResponse.schema()
    )

    response = await agent.ainvoke({"messages": history})
    final_content = response["messages"][-1].content

    try:
        parsed = json.loads(final_content)
    except json.JSONDecodeError:
        # Look for a JSON object in the text
        json_match = re.search(r'\{.*\}', final_content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
        else:
            parsed = {"response": final_content, "resume": None}

    # Validate with Pydantic model
    try:
        ai_response = AIResponse(**parsed)
    except Exception as e:
        # If validation fails, return an error JSON
        ai_response = AIResponse(
            response=f"Error processing response: {e}\nRaw: {final_content}",
            resume=None
        )
    
    
    manager.store_message(session_id, "user", user_input)
    manager.store_message(session_id, "agent", final_content)

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

    close_mysql_service()

if __name__ == "__main__":
    asyncio.run(main())