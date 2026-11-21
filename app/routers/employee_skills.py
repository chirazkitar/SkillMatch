from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee, Skill, EmployeeSkill

from app.schemas.schemas import (
    EmployeeSkillCreate,
    EmployeeSkillUpdate,
    EmployeeSkillResponse
)

router = APIRouter(
    prefix="/employee-skills",
    tags=["Employee Skills"]
)


# =========================
# CREATE EMPLOYEE SKILL
# =========================

@router.post("/", response_model=EmployeeSkillResponse, status_code=201)
def create_employee_skill(
    data: EmployeeSkillCreate,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == data.employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    skill = db.query(Skill).filter(
        Skill.id == data.skill_id
    ).first()

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    existing_association = db.query(EmployeeSkill).filter(
        EmployeeSkill.employee_id == data.employee_id,
        EmployeeSkill.skill_id == data.skill_id
    ).first()

    if existing_association:
        raise HTTPException(
            status_code=400,
            detail="This skill is already assigned to this employee"
        )

    new_association = EmployeeSkill(**data.model_dump())

    db.add(new_association)
    db.commit()
    db.refresh(new_association)

    return new_association


# =========================
# GET ALL ASSOCIATIONS
# =========================

@router.get("/", response_model=list[EmployeeSkillResponse])
def get_employee_skills(db: Session = Depends(get_db)):

    associations = db.query(EmployeeSkill).all()

    return associations


# =========================
# GET ASSOCIATION BY ID
# =========================

@router.get("/{association_id}", response_model=EmployeeSkillResponse)
def get_employee_skill(
    association_id: int,
    db: Session = Depends(get_db)
):

    association = db.query(EmployeeSkill).filter(
        EmployeeSkill.id == association_id
    ).first()

    if association is None:
        raise HTTPException(
            status_code=404,
            detail="Employee skill association not found"
        )

    return association


# =========================
# UPDATE ASSOCIATION
# =========================

@router.put("/{association_id}", response_model=EmployeeSkillResponse)
def update_employee_skill(
    association_id: int,
    data: EmployeeSkillUpdate,
    db: Session = Depends(get_db)
):

    association = db.query(EmployeeSkill).filter(
        EmployeeSkill.id == association_id
    ).first()

    if association is None:
        raise HTTPException(
            status_code=404,
            detail="Employee skill association not found"
        )

    association.level = data.level

    db.commit()
    db.refresh(association)

    return association


# =========================
# DELETE ASSOCIATION
# =========================

@router.delete("/{association_id}", status_code=204)
def delete_employee_skill(
    association_id: int,
    db: Session = Depends(get_db)
):

    association = db.query(EmployeeSkill).filter(
        EmployeeSkill.id == association_id
    ).first()

    if association is None:
        raise HTTPException(
            status_code=404,
            detail="Employee skill association not found"
        )

    db.delete(association)
    db.commit()

    return None

employee_skills_router = APIRouter(
    prefix="/employees",
    tags=["Employee Skills"]
)

@employee_skills_router.get(
    "/{employee_id}/skills",
    response_model=list[EmployeeSkillResponse]
)
def get_skills_by_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    associations = db.query(EmployeeSkill).filter(
        EmployeeSkill.employee_id == employee_id
    ).all()

    return associations

@employee_skills_router.post(
    "/{employee_id}/skills",
    response_model=EmployeeSkillResponse,
    status_code=201
)
def assign_skill_to_employee(
    employee_id: int,
    data: EmployeeSkillUpdate,
    skill_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    skill = db.query(Skill).filter(
        Skill.id == skill_id
    ).first()

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    existing_association = db.query(EmployeeSkill).filter(
        EmployeeSkill.employee_id == employee_id,
        EmployeeSkill.skill_id == skill_id
    ).first()

    if existing_association:
        raise HTTPException(
            status_code=400,
            detail="This skill is already assigned to this employee"
        )

    new_association = EmployeeSkill(
        employee_id=employee_id,
        skill_id=skill_id,
        level=data.level
    )

    db.add(new_association)
    db.commit()
    db.refresh(new_association)

    return new_association

@employee_skills_router.put(
    "/{employee_id}/skills/{skill_id}",
    response_model=EmployeeSkillResponse
)
def update_employee_skill_level(
    employee_id: int,
    skill_id: int,
    data: EmployeeSkillUpdate,
    db: Session = Depends(get_db)
):

    association = db.query(EmployeeSkill).filter(
        EmployeeSkill.employee_id == employee_id,
        EmployeeSkill.skill_id == skill_id
    ).first()

    if association is None:
        raise HTTPException(
            status_code=404,
            detail="Employee skill association not found"
        )

    association.level = data.level

    db.commit()
    db.refresh(association)

    return association

@employee_skills_router.delete(
    "/{employee_id}/skills/{skill_id}",
    status_code=204
)
def remove_skill_from_employee(
    employee_id: int,
    skill_id: int,
    db: Session = Depends(get_db)
):

    association = db.query(EmployeeSkill).filter(
        EmployeeSkill.employee_id == employee_id,
        EmployeeSkill.skill_id == skill_id
    ).first()

    if association is None:
        raise HTTPException(
            status_code=404,
            detail="Employee skill association not found"
        )

    db.delete(association)
    db.commit()

    return None