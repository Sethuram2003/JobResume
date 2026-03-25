from fastapi.responses import JSONResponse
from fastapi import FastAPI, Form, APIRouter
from dotenv import load_dotenv
import uuid
from app.core.agent_logic.agent import chat_agent
from app.core.model import AIResponse

load_dotenv()

chat_agent_router = APIRouter(tags=["ChatAgent"])
app = FastAPI()

@chat_agent_router.post("/chat")
async def chat(
    query: str = Form(...),
    session_id: str = Form(None)  
):
    """
    Process a user query using the dynamic knowledge graph agent.
    If session_id is provided, conversation history is maintained across calls.
    """
    if not session_id:
        session_id = str(uuid.uuid4())

    response = await chat_agent(session_id, query)

    return JSONResponse(content=response.dict(), status_code=200)
