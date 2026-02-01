from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from app.services.debug_services import DebugService


router = APIRouter(prefix="/debug", tags=["debug"])


# ---------------------------------------------------------
# GET DATABASE STATE
# ---------------------------------------------------------
@router.get("/db")
def state_db(db: Session = Depends(get_db)):
    service = DebugService(db)
    return service.get_db_state()


# ---------------------------------------------------------
# CLEAR DATABASE
# ---------------------------------------------------------
@router.delete("/db")
def clear_db(db: Session = Depends(get_db)):
    service = DebugService(db)
    return service.clear_database()