from enum import Enum


class ProjectStatus(str, Enum):
    """Enumeration of project lifecycle stages"""

    PLANNING = "Planning"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class ProjectRoleEnum(str, Enum):
    """Enumeration of access levels within a project"""

    OWNER = "owner"
    COLLABORATOR = "collaborator"
    VIEWER = "viewer"
