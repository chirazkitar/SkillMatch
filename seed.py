from datetime import date

from app.database import Base, engine, SessionLocal
from app.models import (
    Employee,
    Skill,
    EmployeeSkill,
    Role,
    RoleSkill
)


# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:

    # =========================
    # EMPLOYEES
    # =========================

    employees_data = [
        Employee(
            full_name="Ahmed Ben Ali",
            email="ahmed@skillmatch.com",
            department="IT",
            hire_date=date(2023, 3, 15)
        ),
        Employee(
            full_name="Sarra Trabelsi",
            email="sarra@skillmatch.com",
            department="Data",
            hire_date=date(2024, 1, 10)
        ),
        Employee(
            full_name="Youssef Mansouri",
            email="youssef@skillmatch.com",
            department="IT",
            hire_date=date(2022, 6, 1)
        )
    ]

    # =========================
    # SKILLS
    # =========================

    skills_data = [
        Skill(name="Python", category="Programming"),
        Skill(name="SQL", category="Database"),
        Skill(name="FastAPI", category="Backend"),
        Skill(name="Machine Learning", category="AI"),
        Skill(name="Docker", category="DevOps"),
        Skill(name="Power BI", category="Data Analysis")
    ]

    # =========================
    # ROLES
    # =========================

    roles_data = [
        Role(
            title="Backend Developer",
            department="IT",
            description="Develop and maintain backend APIs."
        ),
        Role(
            title="Data Analyst",
            department="Data",
            description="Analyze data and build dashboards."
        ),
        Role(
            title="AI Engineer",
            department="AI",
            description="Develop AI and machine learning solutions."
        )
    ]

    # Insert employees if not already present
    for employee in employees_data:
        existing = db.query(Employee).filter(
            Employee.email == employee.email
        ).first()

        if not existing:
            db.add(employee)

    # Insert skills if not already present
    for skill in skills_data:
        existing = db.query(Skill).filter(
            Skill.name == skill.name
        ).first()

        if not existing:
            db.add(skill)

    # Insert roles if not already present
    for role in roles_data:
        existing = db.query(Role).filter(
            Role.title == role.title
        ).first()

        if not existing:
            db.add(role)

    db.commit()

    # Retrieve saved records
    employees = db.query(Employee).all()
    skills = db.query(Skill).all()
    roles = db.query(Role).all()

    # =========================
    # EMPLOYEE SKILLS
    # =========================

    employee_skills_data = [
        ("ahmed@skillmatch.com", "Python", 4),
        ("ahmed@skillmatch.com", "SQL", 4),
        ("ahmed@skillmatch.com", "FastAPI", 3),
        ("ahmed@skillmatch.com", "Docker", 2),

        ("sarra@skillmatch.com", "Python", 3),
        ("sarra@skillmatch.com", "SQL", 4),
        ("sarra@skillmatch.com", "Power BI", 5),
        ("sarra@skillmatch.com", "Machine Learning", 3),

        ("youssef@skillmatch.com", "Python", 5),
        ("youssef@skillmatch.com", "FastAPI", 4),
        ("youssef@skillmatch.com", "Docker", 4),
        ("youssef@skillmatch.com", "Machine Learning", 4)
    ]

    for email, skill_name, level in employee_skills_data:

        employee = db.query(Employee).filter(
            Employee.email == email
        ).first()

        skill = db.query(Skill).filter(
            Skill.name == skill_name
        ).first()

        existing = db.query(EmployeeSkill).filter(
            EmployeeSkill.employee_id == employee.id,
            EmployeeSkill.skill_id == skill.id
        ).first()

        if not existing:
            db.add(
                EmployeeSkill(
                    employee_id=employee.id,
                    skill_id=skill.id,
                    level=level
                )
            )

    # =========================
    # ROLE SKILLS
    # =========================

    role_skills_data = [
        ("Backend Developer", "Python", 4),
        ("Backend Developer", "SQL", 3),
        ("Backend Developer", "FastAPI", 4),
        ("Backend Developer", "Docker", 3),

        ("Data Analyst", "SQL", 4),
        ("Data Analyst", "Power BI", 4),
        ("Data Analyst", "Python", 3),

        ("AI Engineer", "Python", 4),
        ("AI Engineer", "Machine Learning", 4),
        ("AI Engineer", "SQL", 3)
    ]

    for role_title, skill_name, required_level in role_skills_data:

        role = db.query(Role).filter(
            Role.title == role_title
        ).first()

        skill = db.query(Skill).filter(
            Skill.name == skill_name
        ).first()

        existing = db.query(RoleSkill).filter(
            RoleSkill.role_id == role.id,
            RoleSkill.skill_id == skill.id
        ).first()

        if not existing:
            db.add(
                RoleSkill(
                    role_id=role.id,
                    skill_id=skill.id,
                    required_level=required_level
                )
            )

    db.commit()

    print("Database seeded successfully!")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()