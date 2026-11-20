from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Skill
from app.schemas.schemas import (
    SkillCreate,
    SkillUpdate,
    SkillResponse
)

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)


# =========================
# CREATE SKILL
# =========================

@router.post("/", response_model=SkillResponse, status_code=201)
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):

    existing_skill = db.query(Skill).filter(
        Skill.name == skill.name
    ).first()

    if existing_skill:
        raise HTTPException(
            status_code=400,
            detail="This skill already exists"
        )

    new_skill = Skill(**skill.model_dump())

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


# =========================
# GET ALL SKILLS
# =========================

@router.get("/", response_model=list[SkillResponse])
def get_skills(db: Session = Depends(get_db)):

    skills = db.query(Skill).all()

    return skills


# =========================
# GET SKILL BY ID
# =========================

@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(skill_id: int, db: Session = Depends(get_db)):

    skill = db.query(Skill).filter(
        Skill.id == skill_id
    ).first()

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    return skill


# =========================
# UPDATE SKILL
# =========================

@router.put("/{skill_id}", response_model=SkillResponse)
def update_skill(
    skill_id: int,
    skill_data: SkillUpdate,
    db: Session = Depends(get_db)
):

    skill = db.query(Skill).filter(
        Skill.id == skill_id
    ).first()

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    update_data = skill_data.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing_skill = db.query(Skill).filter(
            Skill.name == update_data["name"],
            Skill.id != skill_id
        ).first()

        if existing_skill:
            raise HTTPException(
                status_code=400,
                detail="Skill name already exists"
            )

    for key, value in update_data.items():
        setattr(skill, key, value)

    db.commit()
    db.refresh(skill)

    return skill


# =========================
# DELETE SKILL
# =========================

@router.delete("/{skill_id}", status_code=204)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):

    skill = db.query(Skill).filter(
        Skill.id == skill_id
    ).first()

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    if skill.employee_skills or skill.role_skills:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete skill because it is associated with employees or roles"
        )

    db.delete(skill)
    db.commit()

    return None