import asyncio
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from app.core.mysql_database.mysql_service import get_mysql_service, close_mysql_service
from app.core.agent_logic.prompts import SYSTEM_PROMPT
from app.core.agent_logic.tools import generate_resume, context_for_resume
from app.core.model import AIResponse, ResumeData
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

    llm = ChatOllama(model="kimi-k2:1t-cloud")

    agent = create_agent(
        llm,
        tools=[generate_resume, context_for_resume],
        system_prompt=SYSTEM_PROMPT
    )

    response = await agent.ainvoke({"messages": history})
    assistant_reply = response["messages"][-1].content
    
    try:
        if isinstance(assistant_reply, str):
            clean_json = assistant_reply.replace("```json", "").replace("```", "").strip()
            parsed_response = AIResponse.model_validate_json(clean_json)
        else:
            parsed_response = AIResponse.model_validate(assistant_reply)
    except Exception as e:
        parsed_response = AIResponse(response=assistant_reply, resume=None)
    manager.store_message(session_id, "user", user_input)
    manager.store_message(session_id, "agent", parsed_response.response)

    return parsed_response

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