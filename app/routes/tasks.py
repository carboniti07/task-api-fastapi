from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.db_models import Task
from app.schemas import MessageResponse, Priority, TaskCreate, TaskList, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=TaskList)
def list_tasks(
    db: DbSession,
    completed: bool | None = None,
    priority: Priority | None = None,
    limit: int = 10,
    offset: int = 0,
) -> TaskList:
    query = select(Task)

    if completed is not None:
        query = query.where(Task.completed == completed)

    if priority is not None:
        query = query.where(Task.priority == priority)

    query = query.order_by(Task.id).limit(limit).offset(offset)

    tasks = db.scalars(query).all()

    return TaskList(tasks=list(tasks))


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: DbSession) -> Task:
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada",
        )

    return task


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate, db: DbSession) -> Task:
    new_task = Task(
        title=task.title,
        completed=task.completed,
        priority=task.priority,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: DbSession,
) -> Task:
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada",
        )

    task.title = updated_task.title
    task.completed = updated_task.completed
    task.priority = updated_task.priority

    db.commit()
    db.refresh(task)

    return task


@router.delete(
    "/{task_id}",
    response_model=MessageResponse,
)
def delete_task(
    task_id: int,
    db: DbSession,
) -> MessageResponse:
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada",
        )

    db.delete(task)
    db.commit()

    return MessageResponse(
        message="Tarefa removida com sucesso",
    )
