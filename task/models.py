from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy.types import Text
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum as PyEnum


class TaskStatus(PyEnum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    responsible_person = Column(Integer, ForeignKey('users.id'))

    responsible_user = relationship("User", backref="tasks")
    executors = Column(ARRAY(Integer))  # Масив з id виконавців
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(Integer, nullable=False)
