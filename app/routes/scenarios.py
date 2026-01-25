from fastapi import APIRouter, HTTPException, Depends
from app.models.scenarios import (
    ScenarioDetail,
    ScenarioSummary,
    EditScenarioRequest,
    CreateScenarioRequest
)
import app.db as db
import app.helpers._utils as _utils
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


##############################
# Get all scenarios
##############################
@router.get("/", response_model=list[ScenarioSummary])
def get_scenarios(user = Depends(get_current_user)):
    user_id = user["id"]

    user_scenarios = [s for s in db.scenarios if s["owner_id"] == user_id]

    summaries = []
    for s in user_scenarios:
        summaries.append({
            "id": s["id"],
            "title": s["title"],
            "short_desc": s["short_desc"],
            "categories": s["categories"],
            "stakeholders": [
                {"id": st["id"], "name": st["name"], "role": st["role"]}
                for st in s["stakeholders"]
            ],
            "seniordev": {
                "id": s["seniordev"]["id"],
                "name": s["seniordev"]["name"]
            }
        })

    return summaries


##############################
# Get a single scenario
##############################
@router.get("/{scenario_id}", response_model=ScenarioDetail)
def get_scenario(scenario_id: int, user = Depends(get_current_user)):
    user_id = user["id"]
    scenario = _utils.get_scenario_or_404(scenario_id, user_id)
    return scenario


##############################
# Reset a scenario
##############################
@router.post("/{scenario_id}/reset")
def reset_scenario(scenario_id: int, user = Depends(get_current_user)):
    user_id = user["id"]

    db.scenarios = [
        s for s in db.scenarios
        if not (s["id"] == scenario_id and s["owner_id"] == user_id)
    ]

    template = next((t for t in db.default_scenarios if t["id"] == scenario_id), None)
    if template is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "TEMPLATE_NOT_FOUND", "message": "Default scenario template missing."}
        )

    new_scenario = _utils.clone_template(template, user_id)
    db.scenarios.append(new_scenario)

    return {"status": "reset"}


##############################
# Get senior dev feedback
##############################
@router.get("/{scenario_id}/devfeedback")
def get_dev_feedback(scenario_id: int, user = Depends(get_current_user)):
    user_id = user["id"]
    scenario = _utils.get_scenario_or_404(scenario_id, user_id)

    return {
        "seniordev_id": scenario["seniordev"]["id"],
        "feedback": scenario["seniordev"].get("feedback", "No feedback yet.")
    }


##############################
# Create a new scenario
##############################
@router.post("/")
def create_scenario(payload: CreateScenarioRequest, user = Depends(get_current_user)):
    user_id = user["id"]

    new_id = max([s["id"] for s in db.scenarios], default=0) + 1

    new_scenario = {
        "id": new_id,
        "owner_id": user_id,
        "title": payload.title,
        "short_desc": payload.short_desc,
        "long_desc": payload.long_desc,
        "categories": payload.categories,
        "stakeholders": [],
        "seniordev": {"id": 0, "name": "Senior Dev", "chat_history": {"messages": []}},
        "requirements": {"items": []},
    }

    db.scenarios.append(new_scenario)
    return {"scenario_id": new_id, "status": "created"}


##############################
# Edit a scenario
##############################
@router.patch("/{scenario_id}")
def edit_scenario(scenario_id: int, payload: EditScenarioRequest, user = Depends(get_current_user)):
    user_id = user["id"]
    scenario = _utils.get_scenario_or_404(scenario_id, user_id)

    for field, value in payload.dict(exclude_unset=True).items():
        scenario[field] = value

    return {"status": "updated"}


##############################
# Delete a scenario
##############################
@router.delete("/{scenario_id}")
def delete_scenario(scenario_id: int, user = Depends(get_current_user)):
    user_id = user["id"]
    scenario = _utils.get_scenario_or_404(scenario_id, user_id)

    db.scenarios.remove(scenario)
    return {"status": "deleted"}


##############################
# Regenerate default scenarios
##############################
@router.post("/regenerate_defaults")
def regenerate_defaults(user = Depends(get_current_user)):
    user_id = user["id"]

    db.scenarios = [s for s in db.scenarios if s["owner_id"] != user_id]

    for t in db.default_scenarios:
        db.scenarios.append(_utils.clone_template(t, user_id))

    return {"status": "regenerated", "count": len(db.default_scenarios)}