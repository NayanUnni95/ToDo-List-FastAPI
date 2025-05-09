from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from ..database.config import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String)
    uname = Column(String)
    password = Column(String)
    task = relationship("Tasks", back_populates="creator")


class Tasks(Base):
    __tablename__ = "tasks"
    taskId = Column(Integer, primary_key=True, default=uuid.uuid4, index=True)
    userId = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String)
    desc = Column(String)
    deadline = Column(DateTime)
    isCompleted = Column(Boolean)
    creator = relationship("Users", back_populates="task")
