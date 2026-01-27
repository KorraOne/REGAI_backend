from fastapi import FastAPI

from app.routes import debug

from app.routes import auth
from app.routes import scenarios
from app.routes import requirements
from app.routes import stakeholders

app = FastAPI()

app.include_router(debug.router)

app.include_router(auth.router)
app.include_router(scenarios.router)
app.include_router(requirements.router)
app.include_router(stakeholders.router)