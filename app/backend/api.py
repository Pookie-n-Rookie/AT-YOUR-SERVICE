from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings
from app.common.logger import get_logger
import traceback

logger = get_logger(__name__)
app = FastAPI(title="AT_YOUR_SERVICE API", version="0.1")


class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.post("/chat")
def chat_endpoint(request: RequestState):
    logger.info(f"Received request for model: {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.error(f"Model {request.model_name} is not allowed.")
        raise HTTPException(status_code=400, detail="Model not allowed.")

    try:
        response = get_response_from_ai_agents(
            llm_id=request.model_name,
            query=request.messages,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
        )
        logger.info(f"Response generated successfully from AI agent: {request.model_name}")
        return {"success": True, "response": response}

    except Exception as e:
        # Log full exception traceback
        tb = traceback.format_exc()
        logger.error(f"Error while generating response from AI agent:\n{tb}")
        raise HTTPException(
            status_code=500,
            detail=f"Backend error: {str(e)}"
        )
