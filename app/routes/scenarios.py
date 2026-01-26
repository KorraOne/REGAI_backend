from fastapi import APIRouter, Depends, HTTPException

from app.models.scenarios import (
    Scenario,
    Category,
    Stakeholder,
    SeniorDev,
    Requirement,
    ScenarioSummary,
    ScenarioDetail,
    CreateScenarioRequest,
    EditScenarioRequest,
    ScenarioCreatedResponse,
    ScenarioUpdatedResponse,
    ScenarioDeletedResponse,
)

import app.db as db
import app.helpers._utils as _utils
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/scenarios", tags=["scenarios"])


# -------------------------
# Helper: normalize scenario
# -------------------------

def normalize_scenario(raw: dict) -> Scenario:
    return Scenario(
        id=raw["id"],
        owner_id=raw["owner_id"],
        title=raw["title"],
        short_desc=raw["short_desc"],
        long_desc=raw["long_desc"],
        categories=[Category(**c) for c in raw["categories"]],
        stakeholders=[Stakeholder(**st) for st in raw["stakeholders"]],
        seniordev=SeniorDev(**raw["seniordev"]),
        requirements=[Requirement(**r) for r in raw["requirements"]],
    )


# -------------------------
# GET all scenarios (summary)
# -------------------------

@router.get("/", response_model=list[ScenarioSummary])
def get_scenarios(user=Depends(get_current_user)):
    user_id = user["id"]

    user_scenarios = [
        normalize_scenario(s)
        for s in db.scenarios
        if s["owner_id"] == user_id
    ]

    summaries = []
    for s in user_scenarios:
        summaries.append(
            ScenarioSummary(
                id=s.id,
                title=s.title,
                short_desc=s.short_desc,
                categories=[c.name for c in s.categories],
                stakeholders=[
                    {"id": st.id, "name": st.name, "role": st.role}
                    for st in s.stakeholders
                ],
                seniordev={"id": s.seniordev.id, "name": s.seniordev.name},
            )
        )

    return summaries


# -------------------------
# GET single scenario (detail)
# -------------------------

@router.get("/{scenario_id}", response_model=ScenarioDetail)
def get_scenario(scenario_id: int, user=Depends(get_current_user)):
    user_id = user["id"]
    raw = _utils.get_scenario_or_404(scenario_id, user_id)
    scenario = normalize_scenario(raw)
    return scenario


# -------------------------
# Create scenario
# -------------------------

@router.post("/", response_model=ScenarioCreatedResponse)
def create_scenario(payload: CreateScenarioRequest, user=Depends(get_current_user)):
    user_id = user["id"]

    new_id = max([s["id"] for s in db.scenarios], default=0) + 1

    new_scenario = {
        "id": new_id,
        "owner_id": user_id,
        "title": payload.title,
        "short_desc": payload.short_desc,
        "long_desc": payload.long_desc,
        "categories": [c.dict() for c in payload.categories],
        "stakeholders": [],
        "seniordev": {
            "id": 0,
            "name": "Senior Dev",
            "role": "Senior Developer",
            "desc": "Your senior developer assistant",
            "chats": {
                "id": 1,
                "messages": []
            }
        },
        "requirements": [],
    }

    db.scenarios.append(new_scenario)
    return ScenarioCreatedResponse(scenario_id=new_id)


# -------------------------
# Edit scenario
# -------------------------

@router.patch("/{scenario_id}", response_model=ScenarioUpdatedResponse)
def edit_scenario(scenario_id: int, payload: EditScenarioRequest, user=Depends(get_current_user)):
    user_id = user["id"]
    scenario = _utils.get_scenario_or_404(scenario_id, user_id)

    for field, value in payload.dict(exclude_unset=True).items():
        scenario[field] = value

    return ScenarioUpdatedResponse()


# -------------------------
# Delete scenario
# -------------------------

@router.delete("/{scenario_id}", response_model=ScenarioDeletedResponse)
def delete_scenario(scenario_id: int, user=Depends(get_current_user)):
    user_id = user["id"]
    scenario = _utils.get_scenario_or_404(scenario_id, user_id)

    db.scenarios.remove(scenario)
    return ScenarioDeletedResponse()