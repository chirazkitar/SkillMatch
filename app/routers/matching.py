
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee, Role
from app.services.matching import calculate_match
from app.schemas.schemas import MatchingResponse


router = APIRouter(
    prefix="/matching",
    tags=["Matching"]
)


# Match one employee with one role
@router.get(
    "/employee/{employee_id}/role/{role_id}",
    response_model=MatchingResponse
)
def match_employee_to_role(
    employee_id: int,
    role_id: int,
    db: Session = Depends(get_db)
):

    result, error = calculate_match(
        db, employee_id, role_id
    )

    if error:
        if error in ["Employee not found", "Role not found"]:
            raise HTTPException(
                status_code=404,
                detail=error
            )

        raise HTTPException(
            status_code=400,
            detail=error
        )

    return result


# Match one employee with all roles
@router.get(
    "/employee/{employee_id}",
    response_model=list[MatchingResponse]
)
def match_employee_to_all_roles(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    roles = db.query(Role).all()

    results = []

    for role in roles:

        result, error = calculate_match(
            db, employee_id, role.id
        )

        if not error:
            results.append(result)

    # Sort roles from the highest match to the lowest
    results.sort(
        key=lambda item: item["match_percentage"],
        reverse=True
    )

    return results


# Rank all employees for one role
@router.get(
    "/role/{role_id}",
    response_model=list[MatchingResponse]
)
def rank_employees_for_role(
    role_id: int,
    db: Session = Depends(get_db)
):

    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    employees = db.query(Employee).all()

    results = []

    for employee in employees:

        result, error = calculate_match(
            db, employee.id, role_id
        )

        if not error:
            results.append(result)

    # Rank employees by compatibility
    results.sort(
        key=lambda item: item["match_percentage"],
        reverse=True
    )

    return results
