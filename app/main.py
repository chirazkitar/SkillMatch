from fastapi import FastAPI

from app.database import engine, Base
from app import models


# Création des tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SkillMatch API",
    description="Platform for skill management and role matching",
    version="1.0.0"
)


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