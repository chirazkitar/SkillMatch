from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship

from app.database import Base


# =========================
# EMPLOYEES
# =========================

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    department = Column(String(100), nullable=False)
    hire_date = Column(Date, nullable=True)

    skills = relationship(
        "EmployeeSkill",
        back_populates="employee",
        cascade="all, delete-orphan"
    )


# =========================
# SKILLS
# =========================

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100), nullable=False)

    employee_skills = relationship(
        "EmployeeSkill",
        back_populates="skill"
    )

    role_skills = relationship(
        "RoleSkill",
        back_populates="skill"
    )


# =========================
# EMPLOYEE SKILLS
# =========================

class EmployeeSkill(Base):
    __tablename__ = "employee_skills"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        nullable=False
    )

    level = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "skill_id",
            name="uq_employee_skill"
        ),
    )

    employee = relationship(
        "Employee",
        back_populates="skills"
    )

    skill = relationship(
        "Skill",
        back_populates="employee_skills"
    )


# =========================
# ROLES
# =========================

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    skills = relationship(
        "RoleSkill",
        back_populates="role",
        cascade="all, delete-orphan"
    )


# =========================
# ROLE SKILLS
# =========================

class RoleSkill(Base):
    __tablename__ = "role_skills"

    id = Column(Integer, primary_key=True, index=True)

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        nullable=False
    )

    required_level = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "skill_id",
            name="uq_role_skill"
        ),
    )

    role = relationship(
        "Role",
        back_populates="skills"
    )

    skill = relationship(
        "Skill",
        back_populates="role_skills"
    )