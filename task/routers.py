from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import APIRouter
from sqlalchemy.orm import Session

from task import models, schemas
from auth import auth
from task.schemas import TaskInDB
from task.models import Task

from config.database import get_db
from tools.email import send_mock_email

router = APIRouter()


@router.get("/tasks/", response_model=List[TaskInDB])
async def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks


@router.post("/tasks/", response_model=schemas.TaskInDB, dependencies=[Depends(auth.admin_required)])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/tasks/{task_id}", response_model=schemas.TaskInDB)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if str(db_task.status) != str(task.dict().get('status')):
        send_mock_email(subject=f"Task changes",
                        body=f"Task {db_task.id} was changed",
                        recipient_email=db_task.responsible_user.email)
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    return db_task


@router.patch("/tasks/{task_id}", response_model=schemas.TaskInDB)
def update_task(task_id: int, task: dict, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.status.value != task.get('status'):
        send_mock_email(subject=f"Task changes",
                        body=f"Task {db_task.id} was changed",
                        recipient_email=db_task.responsible_user.email)
    for key, value in task.items():
        setattr(db_task, key, value)

    db.commit()
    return db_task


@router.delete("/tasks/{task_id}", dependencies=[Depends(auth.admin_required)])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}

