from fastapi import HTTPException, status
from ..model import models


def create_task(request, db, get_current_user):
    new_task = models.Tasks(
        userId=get_current_user.id,
        title=request.title,
        desc=request.desc,
        deadline=request.deadline,
        isCompleted=False,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def view_all_task(db, get_current_user):
    task = (
        db.query(models.Tasks).filter(models.Tasks.userId == get_current_user.id).all()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Empty Task",
        )
    return task


def view_task(taskId, db, get_current_user):
    task = db.query(models.Tasks).filter(models.Tasks.taskId == taskId).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Task not found. Invalid taskId : {taskId}",
        )
    if task.userId != get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this task.",
        )
    return task
