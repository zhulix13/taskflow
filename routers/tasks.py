from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from get_user import get_current_user  # import your auth dependency

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Create a task for the current user
@router.post("/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_task = models.Task(**task.model_dump(), owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# Get all tasks for the current user
@router.get("/", response_model=list[schemas.Task])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks


# Get a specific task (only if owned by current user)
@router.get("/{task_id}", response_model=schemas.Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id, models.Task.owner_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Update a specific task (only if owned by current user)
@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task: schemas.TaskBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id, models.Task.owner_id == current_user.id
    ).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


# Delete a specific task (only if owned by current user)
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id, models.Task.owner_id == current_user.id
    ).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}
