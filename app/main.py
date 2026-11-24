from fastapi import FastAPI

from app.database import engine, Base
from app import models

from app.routers import employees, skills, roles, matching

from app.routers.employee_skills import (
    router as employee_skills_router,
    employee_skills_router as employees_skills_router
)

from app.routers.role_skills import (
    router as role_skills_router,
    role_skills_router as roles_skills_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SkillMatch API",
    description="Platform for skill management and role matching",
    version="1.0.0"
)

app.include_router(employees.router)
app.include_router(skills.router)
app.include_router(roles.router)


app.include_router(employee_skills_router)
app.include_router(employees_skills_router)

app.include_router(role_skills_router)
app.include_router(roles_skills_router)

app.include_router(matching.router)

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