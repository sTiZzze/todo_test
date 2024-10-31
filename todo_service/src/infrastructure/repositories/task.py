from typing import Iterable

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.domain.models.task import Task, TodoList
from src.domain.models.user import User
from src.domain.DTO.task import TaskCreateUpdate, TaskUpdate


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_all(self, entity: Task, user: User) -> Iterable[Task]:
        query = await self.__session.execute(select(entity).join(TodoList).filter(TodoList.user == user))
        return query.scalars().all()

    async def get_by_id(self, entity: Task, user: User, id: int) -> Task:
        query = await self.__session.execute(
            select(entity).join(TodoList).filter(entity.id == id, TodoList.user_id == user.id)
        )
        task = query.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found.")
        return task

    async def create(self, entity: Task, model: TaskCreateUpdate, user: User) -> Task:
        stmt = select(TodoList).filter_by(id=model.todo_list_id, user=user)
        result = await self.__session.execute(stmt)
        todo_list = result.scalar_one()
        if not todo_list:
            raise ValueError("TodoList not found")
        new_task = Task(
            title=model.title,
            description=model.description,
            todo_list=todo_list
        )

        self.__session.add(new_task)
        await self.__session.commit()
        await self.__session.refresh(new_task)

        return new_task

    async def update(self, entity: Task, model: TaskUpdate, user: User, id: int) -> Task:
        task_query = await self.__session.execute(
            select(entity).join(TodoList).filter(entity.id == int(id), TodoList.user_id == int(user.id)))
        result = task_query.scalars().all()
        if not result:
            raise HTTPException(
                status_code=404, detail="Task is not found.")

        stmt = (
            update(entity)
            .where(entity.id == int(id))
            .values(**model.model_dump())
        )
        await self.__session.execute(stmt)
        await self.__session.commit()
        return result
