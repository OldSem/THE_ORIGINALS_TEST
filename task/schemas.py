from pydantic import BaseModel
from typing import List, Optional, Union
from enum import Enum

from base.schemas import AllOptional


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    responsible_person: int
    executors: List[int]
    status: TaskStatus
    priority: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    status: TaskStatus


class TaskInDB(TaskBase):
    id: int

    class Config:
        orm_mode = True