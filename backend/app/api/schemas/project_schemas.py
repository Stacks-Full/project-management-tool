from pydantic import Field

class ProjectBase():
    project_name: str 
    project_id: int
    description: str 
    start_date: str
    end_date: str 
    status: str
    project_owner: str

class ProjectCreate(ProjectBase):
    project_name: str
    start_date: str
    end_date: str
    project_owner: str

class ProjectUpdate(ProjectBase):
    project_name: str
    start_date: str
    end_date: str

class ProjectMember():
    user_id: str
    username: str
    role: str

class ProjectResponse(ProjectBase):
    project_id: int
    project_name: str
    project_owner: int 
    user_role: str
    status: str
    start_date: str

class MemberResponse():
    user_id: int 
    username: str

class ProjectMemberAssignment():
    user_id: str
    role: str

class MemberResponseTeam():
    user_id: int 
    username: str
    role: str

#class ProjectPublic():
#example Holder
