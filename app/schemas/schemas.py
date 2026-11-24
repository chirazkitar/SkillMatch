from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import date


# =========================
# EMPLOYEE SCHEMAS
# =========================

class EmployeeCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    department: str = Field(min_length=2, max_length=100)
    hire_date: date


class EmployeeUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    department: str | None = Field(default=None, min_length=2, max_length=100)
    hire_date: date | None = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    department: str
    hire_date: date


# =========================
# SKILL SCHEMAS
# =========================

class SkillCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2, max_length=100)


class SkillUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    category: str | None = Field(default=None, min_length=2, max_length=100)


class SkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str


# =========================
# ROLE SCHEMAS
# =========================

class RoleCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    department: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5)


class RoleUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    department: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=5)


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    department: str
    description: str

# =========================
# EMPLOYEE SKILLS SCHEMAS
# =========================

class EmployeeSkillCreate(BaseModel):
    employee_id: int = Field(gt=0)
    skill_id: int = Field(gt=0)
    level: int = Field(ge=1, le=5)


class EmployeeSkillUpdate(BaseModel):
    level: int = Field(ge=1, le=5)


class EmployeeSkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    skill_id: int
    level: int

# =========================
# ROLE SKILLS SCHEMAS
# =========================

class RoleSkillCreate(BaseModel):
    role_id: int = Field(gt=0)
    skill_id: int = Field(gt=0)
    required_level: int = Field(ge=1, le=5)


class RoleSkillUpdate(BaseModel):
    required_level: int = Field(ge=1, le=5)


class RoleSkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role_id: int
    skill_id: int
    required_level: int


class MatchedSkill(BaseModel):
    skill: str
    employee_level: int
    required_level: int


class InsufficientSkill(BaseModel):
    skill: str
    employee_level: int
    required_level: int


class MissingSkill(BaseModel):
    skill: str
    required_level: int


class MatchingResponse(BaseModel):
    employee_id: int
    employee_name: str
    role_id: int
    role_title: str
    match_percentage: float
    total_required_skills: int
    matched_skills: list[MatchedSkill]
    insufficient_skills: list[InsufficientSkill]
    missing_skills: list[MissingSkill]
