from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schema import schemas
from ..repository import todo
from ..database.config import get_db
from ..services.Oauth2 import get_current_user

router = APIRouter(tags=["ToDo"])


@router.post("/create")
def create(
    request: schemas.CreateTodo,
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.create_task(request, db, get_current_user)


@router.get("/group")
def create(
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.group_by(db, get_current_user)


@router.get("/view")
def view_all(
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.view_all_task(db, get_current_user)


@router.get("/view/{taskId}")
def view(
    taskId,
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.view_task(taskId, db, get_current_user)


@router.put("/edit")
def edit(
    request: schemas.EditTodo,
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.edit_task(request, db, get_current_user)


@router.put("/mark")
def mark_as_completed(
    taskId,
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.mark_as_completed(taskId, db, get_current_user)


@router.delete("/delete")
def delete(
    taskId,
    db: Session = Depends(get_db),
    get_current_user: schemas.CurrentUser = Depends(get_current_user),
):
    return todo.delete_task(taskId, db, get_current_user)
