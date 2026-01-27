from pydantic import BaseModel

class ScenarioCreatedResponse(BaseModel):
    scenario_id: int
    status: str = "Created."

class ScenarioUpdatedResponse(BaseModel):
    status: str = "Updated."

class ScenarioDeletedResponse(BaseModel):
    status: str = "Deleted."

class AllRequirementsDeletedResponse(BaseModel):
    message: str = "Requirements deleted."

class RequirementUpdatedResponse(BaseModel):
    message: str = "Requirement updated."

class RequirementDeletedResponse(BaseModel):
    message: str = "Requirement deleted."