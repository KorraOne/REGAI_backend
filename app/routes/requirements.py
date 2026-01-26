from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.helpers._utils import get_scenario_or_404

from app.models.scenarios import Requirement, RequirementUpdatedResponse, RequirementDeletedResponse

router = APIRouter(prefix="/scenarios/{scenario_id}/requirements", tags=["requirements"])

# ---------------------------------------------------------
# GET all requirements for a scenario
# ---------------------------------------------------------
@router.get("", response_model=list[Requirement])
def get_requirements(scenario_id: int, user=Depends(get_current_user)):
    user_id = user["id"]
    scenario = get_scenario_or_404(scenario_id, user_id)
    return scenario["requirements"]


# ---------------------------------------------------------
# DELETE all requirements for a scenario
# ---------------------------------------------------------
@router.delete("")
def delete_all_requirements(scenario_id: int, user=Depends(get_current_user)):
    user_id = user["id"]
    scenario = get_scenario_or_404(scenario_id, user_id)

    scenario["requirements"] = []
    return {"message": "All requirements deleted"}


# ---------------------------------------------------------
# GET a single requirement
# ---------------------------------------------------------
@router.get("/{req_id}", response_model=Requirement)
def get_requirement(scenario_id: int, req_id: int, user=Depends(get_current_user)):
    user_id = user["id"]
    scenario = get_scenario_or_404(scenario_id, user_id)

    items = scenario["requirements"]
    if req_id < 0 or req_id >= len(items):
        raise HTTPException(404, "Requirement not found")

    return items[req_id]


# ---------------------------------------------------------
# CREATE a requirement
# ---------------------------------------------------------
@router.post("", response_model=dict)
def create_requirement(scenario_id: int, payload: Requirement, user=Depends(get_current_user)):
    user_id = user["id"]
    scenario = get_scenario_or_404(scenario_id, user_id)

    new_req = payload.dict()
    scenario["requirements"].append(new_req)

    new_id = len(scenario["requirements"]) - 1
    return {"id": new_id, "message": "Requirement added"}


# ---------------------------------------------------------
# UPDATE a requirement
# ---------------------------------------------------------
@router.patch("/{req_id}", response_model=RequirementUpdatedResponse)
def update_requirement(scenario_id: int, req_id: int, payload: Requirement, user=Depends(get_current_user)):
    user_id = user["id"]
    scenario = get_scenario_or_404(scenario_id, user_id)

    items = scenario["requirements"]
    if req_id < 0 or req_id >= len(items):
        raise HTTPException(404, "Requirement not found")

    req = items[req_id]
    for key, value in payload.dict(exclude_unset=True).items():
        req[key] = value

    return {"message": "Requirement updated"}


# ---------------------------------------------------------
# DELETE a single requirement
# ---------------------------------------------------------
@router.delete("/{req_id}", response_model=RequirementDeletedResponse)
def delete_requirement(scenario_id: int, req_id: int, user=Depends(get_current_user)):
    user_id = user["id"]
    scenario = get_scenario_or_404(scenario_id, user_id)

    items = scenario["requirements"]
    if req_id < 0 or req_id >= len(items):
        raise HTTPException(404, "Requirement not found")

    items.pop(req_id)
    return {"message": "Requirement deleted"}