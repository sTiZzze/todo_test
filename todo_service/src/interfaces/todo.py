from fastapi import APIRouter, Depends, status

from config.database import get_db
from src.domain.models.user import User
from src.domain.models.task import TodoList
from src.domain.DTO.task import TodoListCreateUpdate
from src.applications.todo import TodoService
from src.infrastructure.utils.deps import get_current_user

router_todo = APIRouter()


@router_todo.get('/todo')
async def get_todo_lists(user: User = Depends(get_current_user)):
    async with get_db() as session:
        service = TodoService(session)
    return await service.get_todo(TodoList, user)


@router_todo.post('/todo/create', status_code=status.HTTP_201_CREATED)
async def create_todo_list(task: TodoListCreateUpdate, user: dict = Depends(get_current_user)):
    async with get_db() as session:
        service = TodoService(session)
    return await service.create_todo(TodoList, task, user)


@router_todo.put('/todo/{id}')
async def update_todo_list(id: str, task: TodoListCreateUpdate, user: dict = Depends(get_current_user)):
    async with get_db() as session:
        service = TodoService(session)
    return await service.update_todo(TodoList, task, user, id)
