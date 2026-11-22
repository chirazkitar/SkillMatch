from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Role, Skill, RoleSkill

from app.schemas.schemas import (
    RoleSkillCreate,
    RoleSkillUpdate,
    RoleSkillResponse
)

router = APIRouter(
    prefix="/role-skills",
    tags=["Role Skills"]
)


# =========================
# CREATE ROLE SKILL
# =========================

@router.post("/", response_model=RoleSkillResponse, status_code=201)
def create_role_skill(
    data: RoleSkillCreate,
    db: Session = Depends(get_db)
):

    role = db.query(Role).filter(
        Role.id == data.role_id
    ).first()

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    skill = db.query(Skill).filter(
        Skill.id == data.skill_id
    ).first()

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    existing_association = db.query(RoleSkill).filter(
        RoleSkill.role_id == data.role_id,
        RoleSkill.skill_id == data.skill_id
    ).first()

    if existing_association:
        raise HTTPException(
            status_code=400,
            detail="This skill is already required for this role"
        )

    new_association = RoleSkill(**data.model_dump())

    db.add(new_association)
    db.commit()
    db.refresh(new_association)

    return new_association


# =========================
# GET ALL ASSOCIATIONS
# =========================

@router.get("/", response_model=list[RoleSkillResponse])
def get_role_skills(db: Session = Depends(get_db)):

    associations = db.query(RoleSkill).all()

    return associations


# =========================
# GET ASSOCIATION BY ID
# =========================

@router.get("/{association_id}", response_model=RoleSkillResponse)
def get_role_skill(
    association_id: int,
    db: Session = Depends(get_db)
):

    association = db.query(RoleSkill).filter(
        RoleSkill.id == association_id
    ).first()

    if association is None:
        raise HTTPException(
            status_code=404,
            detail="Role skill association not found"
        )

    return association


# =========================
# UPDATE ASSOCIATION
# =========================

@router.put("/{association_id}", response_model=RoleSkillResponse)
def update_role_skill(
    association_id: int,
    data: RoleSkillUpdate,
    db: Session = Depends(get_db)
):

    association = db.query(RoleSkill).filter(
        RoleSkill.id == association_id
    ).first()

    if association is None:
        raise HTTPException(
            status_code=404,
            detail="Role skill association not found"
        )

    association.required_level = data.required_level

    db.commit()
    db.refresh(association)

    return association


# =========================
# DELETE ASSOCIATION
# =========================

@router.delete("/{association_id}", status_code=204)
def delete_role_skill(
    association_id: int,
    db: Session = Depends(get_db)
):

    association = db.query(RoleSkill).filter(
        RoleSkill.id == association_id
    ).first()

    if association is None:
        raise HTTPException(
            status_code=404,
            detail="Role skill association not found"
        )

    db.delete(association)
    db.commit()

    return None

role_skills_router = APIRouter(
    prefix="/roles",
    tags=["Role Skills"]
)

@role_skills_router.get(
    "/{role_id}/skills",
    response_model=list[RoleSkillResponse]
)
def get_skills_by_role(
    role_id: int,
    db: Session = Depends(get_db)
):

    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    associations = db.query(RoleSkill).filter(
        RoleSkill.role_id == role_id
    ).all()

    return associations

@role_skills_router.post(
    "/{role_id}/skills",
    response_model=RoleSkillResponse,
    status_code=201
)
def assign_skill_to_role(
    role_id: int,
    data: RoleSkillUpdate,
    skill_id: int,
    db: Session = Depends(get_db)
):

    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    skill = db.query(Skill).filter(
        Skill.id == skill_id
    ).first()

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    existing_association = db.query(RoleSkill).filter(
        RoleSkill.role_id == role_id,
        RoleSkill.skill_id == skill_id
    ).first()

    if existing_association:
        raise HTTPException(
            status_code=400,
            detail="This skill is already required for this role"
        )

    new_association = RoleSkill(
        role_id=role_id,
        skill_id=skill_id,
        required_level=data.required_level
    )

    db.add(new_association)
    db.commit()
    db.refresh(new_association)

    return new_association

@role_skills_router.put(
    "/{role_id}/skills/{skill_id}",
    response_model=RoleSkillResponse
)
def update_role_skill_level(
    role_id: int,
    skill_id: int,
    data: RoleSkillUpdate,
    db: Session = Depends(get_db)
):

    association = db.query(RoleSkill).filter(
        RoleSkill.role_id == role_id,
        RoleSkill.skill_id == skill_id
    ).first()

    if association is None:
        raise HTTPException(
            status_code=404,
            detail="Role skill association not found"
        )

    association.required_level = data.required_level

    db.commit()
    db.refresh(association)

    return association

@role_skills_router.delete(
    "/{role_id}/skills/{skill_id}",
    status_code=204
)
def remove_skill_from_role(
    role_id: int,
    skill_id: int,
    db: Session = Depends(get_db)
):

    association = db.query(RoleSkill).filter(
        RoleSkill.role_id == role_id,
        RoleSkill.skill_id == skill_id
    ).first()

    if association is None:
        raise HTTPException(
            status_code=404,
            detail="Role skill association not found"
        )

    db.delete(association)
    db.commit()

    return None