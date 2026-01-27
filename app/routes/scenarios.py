from fastapi import APIRouter, Depends

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
    ChatHistory,
)

import app.db as db
import app.helpers._utils as _utils
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/scenarios", tags=["scenarios"])


# -------------------------
# GET all scenarios (summary)
# -------------------------

@router.get("/", response_model=list[ScenarioSummary])
def get_scenarios(user=Depends(get_current_user)):
    user_id = user["id"]

    user_scenarios = [
        s for s in db.scenarios
        if s.owner_id == user_id
    ]

    summaries: list[ScenarioSummary] = []
    for s in user_scenarios:
        summaries.append(
            ScenarioSummary(
                id=s.id,
                title=s.title,
                short_desc=s.short_desc,
                categories=s.categories,
                stakeholders=[
                    {
                        "id": st.id,
                        "name": st.name,
                        "role": st.role,
                        "desc": st.desc,
                    }
                    for st in s.stakeholders
                ],
                seniordev={
                    "id": s.seniordev.id,
                    "name": s.seniordev.name,
                    "role": s.seniordev.role,
                    "desc": s.seniordev.desc,
                },
            )
        )

    return summaries


# -------------------------
# GET single scenario (detail)
# -------------------------

@router.get("/{scenario_id}", response_model=ScenarioDetail)
def get_scenario(scenario_id: int, user=Depends(get_current_user)):
    user_id = user["id"]
    scenario = _utils.get_scenario_or_404(scenario_id, user_id)
    return scenario  # already a Pydantic model


# -------------------------
# Create scenario
# -------------------------

@router.post("/", response_model=ScenarioCreatedResponse)
def create_scenario(payload: CreateScenarioRequest, user=Depends(get_current_user)):
    user_id = user["id"]

    new_id = max([s.id for s in db.scenarios], default=0) + 1

    new_scenario = Scenario(
        id=new_id,
        owner_id=user_id,
        title=payload.title,
        short_desc=payload.short_desc,
        long_desc=payload.long_desc,
        categories=payload.categories,
        stakeholders=[
            Stakeholder(
                id=st.id,
                name=st.name,
                role=st.role,
                desc=st.desc,
                chats=ChatHistory(id=1, messages=[]),
            )
            for st in payload.stakeholders
        ],
        seniordev=SeniorDev(
            id=0,
            name="Senior Dev",
            role="Senior Developer",
            desc="Your senior developer assistant",
            chats=ChatHistory(id=1, messages=[]),
        ),
        requirements=[],
    )

    db.scenarios.append(new_scenario)
    return ScenarioCreatedResponse(scenario_id=new_id)


# -------------------------
# Edit scenario
# -------------------------

@router.patch("/{scenario_id}", response_model=ScenarioUpdatedResponse)
def edit_scenario(scenario_id: int, payload: EditScenarioRequest, user=Depends(get_current_user)):
    user_id = user["id"]
    scenario = _utils.get_scenario_or_404(scenario_id, user_id)

    data = payload.dict(exclude_unset=True)

    # Update simple fields
    if "title" in data and data["title"] is not None:
        scenario.title = data["title"]

    if "short_desc" in data and data["short_desc"] is not None:
        scenario.short_desc = data["short_desc"]

    if "long_desc" in data and data["long_desc"] is not None:
        scenario.long_desc = data["long_desc"]

    # Update categories
    if "categories" in data and data["categories"] is not None:
        scenario.categories = data["categories"]

    # Update stakeholders
    if "stakeholders" in data and data["stakeholders"] is not None:
        updated = []
        for st in data["stakeholders"]:
            st_dict = st.dict() if hasattr(st, "dict") else st

            existing = next((x for x in scenario.stakeholders if x.id == st_dict["id"]), None)

            updated.append(
                Stakeholder(
                    id=st_dict["id"],
                    name=st_dict["name"],
                    role=st_dict["role"],
                    desc=st_dict["desc"],
                    chats=existing.chats if existing else ChatHistory(id=1, messages=[]),
                )
            )

        scenario.stakeholders = updated

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