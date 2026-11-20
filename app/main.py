from fastapi import FastAPI

from app.database import engine, Base
from app import models

from app.routers import employees, skills, roles

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SkillMatch API",
    description="Platform for skill management and role matching",
    version="1.0.0"
)

app.include_router(employees.router)
app.include_router(skills.router)
app.include_router(roles.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to SkillMatch API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }