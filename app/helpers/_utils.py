from fastapi import HTTPException
from passlib.context import CryptContext
import app.db as db
import time

from app.models.scenarios.domain.scenario import Scenario, Stakeholder
from app.models.scenarios.domain.chat import ChatHistory, ChatMessage

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------------------------
# AUTH HELPERS
# ---------------------------------------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def email_exists(email: str):
    return any(u.email.lower() == email.lower() for u in db.users)


# ---------------------------------------------------------
# SCENARIO HELPERS (model-based)
# ---------------------------------------------------------

def get_scenario_or_404(scenario_id: int, user_id: int) -> Scenario:
    scenario = next(
        (s for s in db.scenarios if s.id == scenario_id and s.owner_id == user_id),
        None
    )

    if scenario is None:
        raise HTTPException(
            404,
            {"code": "SCENARIO_NOT_FOUND", "message": "Scenario does not exist for this user."}
        )

    return scenario


def ensure_owner(scenario: Scenario, user_id: int):
    if scenario.owner_id != user_id:
        raise HTTPException(
            403,
            {"code": "NOT_OWNER", "message": "You do not own this scenario."}
        )


# ---------------------------------------------------------
# STAKEHOLDER HELPERS (model-based)
# ---------------------------------------------------------

def get_stakeholder_or_404(scenario: Scenario, stakeholder_id: int) -> Stakeholder:
    stakeholder = next(
        (s for s in scenario.stakeholders if s.id == stakeholder_id),
        None
    )

    if stakeholder is None:
        raise HTTPException(
            404,
            {"code": "STAKEHOLDER_NOT_FOUND", "message": "Stakeholder not found in this scenario"}
        )

    return stakeholder


# ---------------------------------------------------------
# CHAT HELPERS (model-based)
# ---------------------------------------------------------

def get_chat_or_404(stakeholder: Stakeholder) -> ChatHistory:
    chat = stakeholder.chats

    if chat is None:
        raise HTTPException(
            500,
            {
                "code": "CHAT_NOT_INITIALIZED",
                "message": "Chat history missing for this stakeholder"
            }
        )

    return chat


def add_chat_message(chat: ChatHistory, sender: str, message: str) -> ChatMessage:
    new_id = len(chat.messages) + 1

    msg = ChatMessage(
        id=new_id,
        sender=sender,
        timestamp=time.time(),
        message=message
    )

    chat.messages.append(msg)
    return msg


# ---------------------------------------------------------
# SCENARIO TEMPLATE CLONING (optional)
# ---------------------------------------------------------

def clone_template(template: Scenario, user_id: int) -> Scenario:
    new_scenario = template.model_copy(deep=True)
    new_scenario.owner_id = user_id
    return new_scenario