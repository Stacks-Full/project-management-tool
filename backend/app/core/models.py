from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from app.core.enums import ProjectStatus, ProjectRoleEnum

class User(SQLModel, table=True):
    """
    Represents a user entity in the database.
    This is the core model for tracking user details
    """
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(index=True, max_length=255)
    email: str = Field(index=True, unique=True, max_length=255)
    username: str = Field(index=True, unique=True, max_length=50)
    hashed_password: str = Field(index=False, max_length=255)
    user_token: Optional[str] = Field(default=None, max_length=1024)

    project_roles: List["ProjectRole"] = Relationship(back_populates="user")


class Project(SQLModel, table=True):
    """Represents a project entity in the database"""
    __tablename__ = "projects"

    project_id: Optional[int] = Field(default=None, primary_key=True)
    project_name: str = Field(index=True, max_length=30)
    description: Optional[str] = Field(default=None, max_length=500)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    status: ProjectStatus = Field(default=ProjectStatus.PLANNING)
    
    project_owner: int = Field(foreign_key="users.user_id")

    members: List["ProjectRole"] = Relationship(back_populates="project")


class ProjectRole(SQLModel, table=True):
    """Link table to manage User roles within Projects"""
    __tablename__ = "project_roles"

    role_id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.project_id")
    user_id: int = Field(foreign_key="users.user_id")
    role: ProjectRoleEnum = Field(default=ProjectRoleEnum.VIEWER)

    user: "User" = Relationship(back_populates="project_roles")
    project: "Project" = Relationship(back_populates="members")
