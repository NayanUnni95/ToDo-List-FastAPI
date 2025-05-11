"""
This module defines the API routes for managing ToDo tasks using FastAPI.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schema import schemas
from ..repository import todo
from ..database.config import get_db
from ..services.Oauth2 import get_current_user

router = APIRouter(tags=["ToDo"])


"""
 - POST /create: Creates a new ToDo task using the provided request data.
"""


@router.post("/create")
def create(
    request: schemas.CreateTodo,
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.create_task(request, db, get_current_user)


"""
- GET /group: Groups tasks based on certain criteria.
"""


@router.get("/group")
def group_task(
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.group_by(db, get_current_user)


"""
- GET /view: Retrieves all ToDo tasks for the current user.
"""


@router.get("/view")
def view_all(
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.view_all_task(db, get_current_user)


"""
- GET /view/{taskId}: Updates an existing ToDo task with the provided data.
"""


@router.get("/view/{taskId}")
def view(
    taskId,
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.view_task(taskId, db, get_current_user)


"""
- PUT /edit: Retrieves a specific ToDo task by its ID.
"""


@router.put("/edit")
def edit(
    request: schemas.EditTodo,
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.edit_task(request, db, get_current_user)


"""
- PUT /mark: Marks a specific ToDo task as completed.
"""


@router.put("/mark")
def mark_as_completed(
    taskId,
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.mark_as_completed(taskId, db, get_current_user)


"""
- DELETE /delete: Deletes a specific ToDo task.
"""


@router.delete("/delete")
def delete(
    taskId,
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.delete_task(taskId, db, get_current_user)
