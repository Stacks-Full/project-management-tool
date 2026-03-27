from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List
from app.core.enums import ProjectStatus, ProjectRoleEnum


class MemberResponse(BaseModel):
    """User data representing a member assigned to a project"""

    user_id: int
    username: str
    role: ProjectRoleEnum

    class Config:
        """Configuration to work with ORM objects."""

        from_attributes = True


class ProjectPublic(BaseModel):
    """The baseline project information visible to the general public"""

    project_name: str = Field(..., max_length=30, description="The name of the project")
    description: Optional[str] = Field(None, description="A brief summary of the project's goals")
    end_date: Optional[date] = Field(None, description="The expected completion date")
    status: ProjectStatus = Field(ProjectStatus.PLANNING, description="Current lifecycle state")

    class Config:
        """Configuration to work with ORM objects."""

        from_attributes = True


class ProjectCreate(ProjectPublic):
    """Data required to initialize a new project, extending the public base class"""

    start_date: Optional[date] = Field(None, description="The date work is scheduled to begin")


class ProjectResponse(ProjectCreate):
    """Detailed view for Team Members: includes IDs, roles, and the full team list"""

    project_id: int
    project_owner: int = Field(..., description="The User ID of the project creator")
    user_role: Optional[ProjectRoleEnum] = Field(
        None, description="The role of the requesting user"
    )
    team_members: List[MemberResponse] = Field(
        default=[], description="List of all users assigned to this project"
    )


class ProjectUpdate(BaseModel):
    """Used for PATCH/PUT. Users can update one field or all"""

    project_name: Optional[str] = Field(None, max_length=30)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    end_date: Optional[date] = None


class ProjectMemberAssignment(BaseModel):
    """To assign a new user to a project or update an existing member's role"""

    user_id: int
    role: ProjectRoleEnum
