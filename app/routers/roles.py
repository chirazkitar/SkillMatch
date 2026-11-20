from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Role
from app.schemas.schemas import (
    RoleCreate,
    RoleUpdate,
    RoleResponse
)

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


# =========================
# CREATE ROLE
# =========================

@router.post("/", response_model=RoleResponse, status_code=201)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):

    new_role = Role(**role.model_dump())

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


# =========================
# GET ALL ROLES
# =========================

@router.get("/", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):

    roles = db.query(Role).all()

    return roles


# =========================
# GET ROLE BY ID
# =========================

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):

    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    return role


# =========================
# UPDATE ROLE
# =========================

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role_data: RoleUpdate,
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

    update_data = role_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(role, key, value)

    db.commit()
    db.refresh(role)

    return role


# =========================
# DELETE ROLE
# =========================

@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: int, db: Session = Depends(get_db)):

    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    if role.role_skills:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete role because it has associated skills"
        )

    db.delete(role)
    db.commit()

    return None