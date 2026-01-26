from fastapi import APIRouter
import app.db as db

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/db")
def state_db():
    return {
        "users": db.users,
        "scenarios": db.scenarios
    }

@router.delete("/db")
def clear_db():
    db.users.clear()
    db.scenarios.clear()
    db.requirements.clear()
    return {"status": "cleared"}