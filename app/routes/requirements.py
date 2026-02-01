# from fastapi import APIRouter, Depends, HTTPException
# from app.auth.dependencies import get_current_user
# from app.helpers._utils import get_scenario_or_404

# from app.models.scenarios.domain.requirement import Requirement

# from app.models.scenarios.dto.create import RequirementCreateRequest
# from app.models.scenarios.dto. responses import AllRequirementsDeletedResponse, RequirementUpdatedResponse, RequirementDeletedResponse
# from app.models.scenarios.dto.update import RequirementUpdateRequest

# router = APIRouter(prefix="/scenarios/{scenario_id}/requirements", tags=["requirements"])


# # -------------------------
# # GET all requirements
# # -------------------------

# @router.get("/", response_model=list[Requirement])
# def get_requirements(scenario_id: int, user=Depends(get_current_user)):
#     scenario = get_scenario_or_404(scenario_id, user.id)
#     return scenario.requirements


# # -------------------------
# # DELETE all requirements
# # -------------------------

# @router.delete("/", response_model=AllRequirementsDeletedResponse)
# def delete_all_requirements(scenario_id: int, user=Depends(get_current_user)):
#     scenario = get_scenario_or_404(scenario_id, user.id)
#     scenario.requirements = []
#     return AllRequirementsDeletedResponse(message="All requirements deleted")


# # -------------------------
# # GET single requirement
# # -------------------------

# @router.get("/{req_id}", response_model=Requirement)
# def get_requirement(scenario_id: int, req_id: int, user=Depends(get_current_user)):
#     scenario = get_scenario_or_404(scenario_id, user.id)

#     req = next((r for r in scenario.requirements if r.id == req_id), None)
#     if not req:
#         raise HTTPException(404, "Requirement not found")

#     return req


# # -------------------------
# # CREATE requirement
# # -------------------------

# @router.post("/", response_model=Requirement)
# def create_requirement(
#     scenario_id: int,
#     payload: RequirementCreateRequest,
#     user=Depends(get_current_user),
# ):
#     scenario = get_scenario_or_404(scenario_id, user.id)

#     new_id = max([r.id for r in scenario.requirements], default=0) + 1

#     new_req = Requirement(
#         id=new_id,
#         type=payload.type,
#         info=payload.info,
#     )

#     scenario.requirements.append(new_req)
#     return new_req


# # -------------------------
# # UPDATE requirement
# # -------------------------

# @router.patch("/{req_id}", response_model=RequirementUpdatedResponse)
# def update_requirement(
#     scenario_id: int,
#     req_id: int,
#     payload: RequirementUpdateRequest,
#     user=Depends(get_current_user),
# ):
#     scenario = get_scenario_or_404(scenario_id, user.id)

#     req = next((r for r in scenario.requirements if r.id == req_id), None)
#     if not req:
#         raise HTTPException(404, "Requirement not found")

#     # Update fields directly from the Pydantic model
#     if payload.type is not None:
#         req.type = payload.type

#     if payload.info is not None:
#         req.info = payload.info

#     return RequirementUpdatedResponse(message="Requirement updated")


# # -------------------------
# # DELETE requirement
# # -------------------------

# @router.delete("/{req_id}", response_model=RequirementDeletedResponse)
# def delete_requirement(scenario_id: int, req_id: int, user=Depends(get_current_user)):
#     scenario = get_scenario_or_404(scenario_id, user.id)

#     index = next((i for i, r in enumerate(scenario.requirements) if r.id == req_id), None)
#     if index is None:
#         raise HTTPException(404, "Requirement not found")

#     scenario.requirements.pop(index)
#     return RequirementDeletedResponse(message="Requirement deleted")