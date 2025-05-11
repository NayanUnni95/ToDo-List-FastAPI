"""
This module provides repository functions for managing tasks in a To-Do List application using FastAPI.
"""

from fastapi import HTTPException, status
from ..model import models
from typing import List
from datetime import datetime

"""
create_task(request, db, get_current_user):
    Creates a new task for the currently authenticated user.
"""


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


"""
group_by(db, get_current_user):
    Groups tasks of the currently authenticated user into pending, completed, and time-elapsed categories.
"""


def group_by(db, get_current_user):
    task = (
        db.query(models.Tasks).filter(models.Tasks.userId == get_current_user.id).all()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Empty Task",
        )
    pending: List = []
    completed: List = []
    timeElapsed: List = []
    for data in task:
        if not data.isCompleted:
            if data.deadline < datetime.now():
                timeElapsed.append(data)
            else:
                pending.append(data)
        elif data.isCompleted:
            completed.append(data)
    return {"pending": pending, "completed": completed, "timeElapsed": timeElapsed}


"""
view_all_task(db, get_current_user):
    Retrieves all tasks for the currently authenticated user.
"""


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


"""
view_task(taskId, db, get_current_user):
    Retrieves a specific task by its ID for the currently authenticated user.
"""


def view_task(taskId, db, get_current_user):
    task = (
        db.query(models.Tasks)
        .filter(
            models.Tasks.taskId == taskId, models.Tasks.userId == get_current_user.id
        )
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo not found. Invalid taskId : {taskId}",
        )
    return task


"""
edit_task(request, db, get_current_user):
    Updates the details of an existing task for the currently authenticated user.
"""


def edit_task(request, db, get_current_user):
    update_todo: dict = {
        "title": request.title,
        "desc": request.desc,
        "deadline": request.deadline,
        "isCompleted": request.isCompleted,
    }
    task = (
        db.query(models.Tasks)
        .filter(
            models.Tasks.userId == get_current_user.id,
            models.Tasks.taskId == request.taskId,
        )
        .update(
            update_todo,
            synchronize_session=False,
        )
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo not found. Invalid taskId : {request.taskId}",
        )
    db.commit()
    return {"message": "Todo content successfully updated."}


"""
delete_task(taskId, db, get_current_user):
    Deletes a specific task by its ID for the currently authenticated user.
"""


def delete_task(taskId, db, get_current_user):
    todo = (
        db.query(models.Tasks)
        .filter(
            models.Tasks.userId == get_current_user.id,
            models.Tasks.taskId == taskId,
        )
        .delete(synchronize_session=False)
    )
    if todo == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found. Invalid taskId : {taskId}",
        )
    db.commit()
    return {"message": "Todo successfully deleted."}


"""
mark_as_completed(taskId, db, get_current_user):
    Marks a specific task as completed for the currently authenticated user.
"""


def mark_as_completed(taskId, db, get_current_user):
    update_todo: dict = {
        "isCompleted": True,
    }
    task = (
        db.query(models.Tasks)
        .filter(
            models.Tasks.userId == get_current_user.id,
            models.Tasks.taskId == taskId,
        )
        .update(
            update_todo,
            synchronize_session=False,
        )
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo not found. Invalid taskId : {taskId}",
        )
    db.commit()
    return {"message": "Todo marked as completed."}
