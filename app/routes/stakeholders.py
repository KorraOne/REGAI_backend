from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.scenarios import ChatHistory, ChatMessage, ChatMessageRequest
from app.helpers._utils import get_scenario_or_404, get_stakeholder_or_404, add_chat_message

router = APIRouter(prefix="/scenarios/{scenario_id}/stakeholders/{stakeholder_id}", tags=["stakeholders"])


@router.get("/chat", response_model=ChatHistory)
def get_chat_history(scenario_id: int, stakeholder_id: int, user=Depends(get_current_user)):
    scenario = get_scenario_or_404(scenario_id, user["id"])
    stakeholder = get_stakeholder_or_404(scenario, stakeholder_id)
    return stakeholder.chats  # already a ChatHistory model


@router.get("/chat/last", response_model=ChatMessage | None)
def get_last_chat(scenario_id: int, stakeholder_id: int, user=Depends(get_current_user)):
    scenario = get_scenario_or_404(scenario_id, user["id"])
    stakeholder = get_stakeholder_or_404(scenario, stakeholder_id)

    if not stakeholder.chats.messages:
        return None

    return stakeholder.chats.messages[-1]


@router.post("/chat", response_model=ChatMessage)
def send_message(scenario_id: int, stakeholder_id: int, request: ChatMessageRequest, user=Depends(get_current_user)):
    scenario = get_scenario_or_404(scenario_id, user["id"])
    stakeholder = get_stakeholder_or_404(scenario, stakeholder_id)
    chat = stakeholder.chats

    # user message
    add_chat_message(chat, "User", request.message)

    # mock LLM
    llm_text = f"I received your message: '{request.message}'. (mock response)"
    llm_msg = add_chat_message(chat, "LLM", llm_text)

    return llm_msg  # already a ChatMessage model