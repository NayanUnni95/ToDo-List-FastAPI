"""
This module defines the SQLModel ORM models for the ToDo List FastAPI application.
"""

from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import Optional, List
from datetime import datetime

"""
Represents the tasks created by users.
"""


class Tasks(SQLModel, table=True):
    __tablename__ = "tasks"
    taskId: int = Field(primary_key=True, unique=True, nullable=False, index=True)
    userId: UUID = Field(foreign_key="users.id")
    title: str
    desc: str
    deadline: datetime
    isCompleted: bool = Field(default=False)
    creator: Optional["Users"] = Relationship(back_populates="task")
    model_config = {"arbitrary_types_allowed": True}


"""
Represents the users of the application.
"""


class Users(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(
        primary_key=True, default_factory=uuid4, unique=True, nullable=False, index=True
    )
    name: str
    uname: Optional[str]
    password: str
    task: Optional[List[Tasks]] = Relationship(back_populates="creator")
    model_config = {"arbitrary_types_allowed": True}
