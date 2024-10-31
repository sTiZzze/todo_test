from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder

from config.database import get_db
from src.domain.models.task import Task
from src.domain.DTO.task import TaskCreateUpdate, TaskUpdate
from src.applications.task import TaskService
from src.infrastructure.utils.deps import get_current_user


router_task = APIRouter()


@router_task.get('/tasks/{id}/')
async def get_task_by_id(id: int, user: dict = Depends(get_current_user)):
    async with get_db() as session:
        service = TaskService(session)
    return await service.get_task_by_id(Task, user, id)


@router_task.get('/tasks/list')
async def get_tasks(user: dict = Depends(get_current_user)):
    async with get_db() as session:
        service = TaskService(session)
    return await service.get_task(Task, user)


@router_task.post('/tasks/create', status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreateUpdate, user: dict = Depends(get_current_user)):
    async with get_db() as session:
        service = TaskService(session)
    data = await service.create_task(Task, task, user)
    return data


@router_task.patch('/tasks/{id}/update')
async def update_task(id: str, task: TaskUpdate, user: dict = Depends(get_current_user)):
    async with get_db() as session:
        service = TaskService(session)
    return await service.update_task(Task, task, user, id)
