"""
This module defines the API routes for managing ToDo tasks using FastAPI.
"""

from fastapi import APIRouter, Depends
from ..schema import schemas
from ..repository import todo
from ..database.config import SessionDep
from ..services.Oauth2 import get_current_user

router = APIRouter(tags=["ToDo"])


"""
 - POST /create: Creates a new ToDo task using the provided request data.
"""


@router.post("/create")
def create(
    request: schemas.CreateTodo,
    session: SessionDep,
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.create_task(request, session, get_current_user)


"""
- GET /group: Groups tasks based on certain criteria.
"""


@router.get("/group")
def group_task(
    session: SessionDep,
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.group_by(session, get_current_user)


"""
- GET /view: Retrieves all ToDo tasks for the current user.
"""


@router.get("/view")
def view_all(
    session: SessionDep,
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.view_all_task(session, get_current_user)


"""
- GET /view/{taskId}: Updates an existing ToDo task with the provided data.
"""


@router.get("/view/{taskId}")
def view(
    taskId,
    session: SessionDep,
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.view_task(taskId, session, get_current_user)


"""
- PUT /edit: Retrieves a specific ToDo task by its ID.
"""


@router.put("/edit")
def edit(
    request: schemas.EditTodo,
    session: SessionDep,
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.edit_task(request, session, get_current_user)


"""
- PUT /mark: Marks a specific ToDo task as completed.
"""


@router.put("/mark")
def mark_as_completed(
    taskId,
    session: SessionDep,
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.mark_as_completed(taskId, session, get_current_user)


"""
- DELETE /delete: Deletes a specific ToDo task.
"""


@router.delete("/delete")
def delete(
    taskId,
    session: SessionDep,
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.delete_task(taskId, session, get_current_user)
