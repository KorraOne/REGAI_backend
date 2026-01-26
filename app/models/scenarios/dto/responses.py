from pydantic import BaseModel

class ScenarioCreatedResponse(BaseModel):
    scenario_id: int
    status: str = "created"

class ScenarioUpdatedResponse(BaseModel):
    status: str = "updated"

class ScenarioDeletedResponse(BaseModel):
    status: str = "deleted"

class RequirementUpdatedResponse(BaseModel):
    message: str = "Requirement updated"

class RequirementDeletedResponse(BaseModel):
    message: str = "Requirement deleted"