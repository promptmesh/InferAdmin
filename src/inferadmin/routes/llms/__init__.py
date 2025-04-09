from fastapi import APIRouter
from datetime import datetime
import uuid
from .models import GetLlmsResponse, CompletionRequest, CompletionResponse
from .support import get_all_llms, generate_completion


router = APIRouter(prefix="/llms")


@router.get("/list")
async def get_llms() -> GetLlmsResponse:
    """List all LLM models deployed by InferAdmin"""
    llms = get_all_llms()
    return GetLlmsResponse(llms=llms)


@router.post("/completion")
async def create_completion(request: CompletionRequest) -> CompletionResponse:
    """Generate a completion from an LLM model"""
    try:
        # This would call the actual implementation once developed
        # Currently returns a 501 Not Implemented error from generate_completion
        text = generate_completion(
            model_id=request.model_id,
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            stop=request.stop
        )
        
        # The following code is unreachable in the current implementation
        # but shows what would be returned when implemented
        return CompletionResponse(
            id=f"cmpl-{str(uuid.uuid4())[:8]}",
            model_id=request.model_id,
            text=text,
            created=datetime.now(),
            usage={
                "prompt_tokens": 0,  # Placeholder
                "completion_tokens": 0,  # Placeholder
                "total_tokens": 0,  # Placeholder
            }
        )
    except Exception:
        # The generate_completion function will raise HTTPException
        # which FastAPI will properly handle
        raise