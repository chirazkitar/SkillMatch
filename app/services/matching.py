
from app.models import Employee, Skill, EmployeeSkill, Role, RoleSkill


def calculate_match(db, employee_id: int, role_id: int):

    # 1. Verify that the employee exists
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        return None, "Employee not found"

    # 2. Verify that the role exists
    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if not role:
        return None, "Role not found"

    # 3. Retrieve the employee's skills
    employee_skills = db.query(
        EmployeeSkill, Skill
    ).join(
        Skill, EmployeeSkill.skill_id == Skill.id
    ).filter(
        EmployeeSkill.employee_id == employee_id
    ).all()

    # Create a dictionary: skill name -> employee level
    employee_skill_map = {
        skill.name: association.level
        for association, skill in employee_skills
    }

    # 4. Retrieve the role's required skills
    role_skills = db.query(
        RoleSkill, Skill
    ).join(
        Skill, RoleSkill.skill_id == Skill.id
    ).filter(
        RoleSkill.role_id == role_id
    ).all()

    if not role_skills:
        return None, "This role has no required skills"

    # 5. Analyze each required skill
    matched_skills = []
    insufficient_skills = []
    missing_skills = []

    total_score = 0

    for association, skill in role_skills:

        required_level = association.required_level
        employee_level = employee_skill_map.get(skill.name)

        if employee_level is None:

            # The employee does not have this skill
            missing_skills.append({
                "skill": skill.name,
                "required_level": required_level
            })

            skill_score = 0

        elif employee_level >= required_level:

            # The skill is mastered at the required level
            matched_skills.append({
                "skill": skill.name,
                "employee_level": employee_level,
                "required_level": required_level
            })

            skill_score = 1

        else:

            # The employee has the skill but needs improvement
            insufficient_skills.append({
                "skill": skill.name,
                "employee_level": employee_level,
                "required_level": required_level
            })

            skill_score = employee_level / required_level

        total_score += skill_score

    # 6. Calculate the overall percentage
    match_percentage = round(
        (total_score / len(role_skills)) * 100,
        2
    )

    # 7. Return the analysis
    return {
        "employee_id": employee.id,
        "employee_name": employee.full_name,
        "role_id": role.id,
        "role_title": role.title,
        "match_percentage": match_percentage,
        "total_required_skills": len(role_skills),
        "matched_skills": matched_skills,
        "insufficient_skills": insufficient_skills,
        "missing_skills": missing_skills
    }, None
