from typing import Iterable

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.domain.models.task import TodoList
from src.domain.models.user import User
from src.domain.DTO.task import TodoListCreateUpdate


class TodoListRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_all(self, entity: TodoList, user: User) -> Iterable[TodoList]:
        query = await self.__session.execute(select(entity).filter(entity.user_id == user.id))
        return query.scalars().all()

    async def create(self, entity: TodoList, model: TodoListCreateUpdate, user: User) -> TodoList:
        model.user_id = user.id
        new_task = entity(**model.model_dump())
        self.__session.add(new_task)
        await self.__session.commit()
        await self.__session.refresh(new_task)
        return new_task

    async def update(self, entity: TodoList, model: TodoListCreateUpdate, user: User, id: int) -> TodoList:
        task_query = await self.__session.execute(
            select(entity).filter(entity.id == int(id), entity.user_id == int(user.id)))
        result = task_query.scalars().all()
        if not result:
            raise HTTPException(
                status_code=404, detail="TodoList is not found.")

        model.user_id = user.id
        stmt = (
            update(entity)
            .where(entity.id == int(id), entity.user_id == int(user.id))
            .values(**model.model_dump())
        )
        await self.__session.execute(stmt)
        await self.__session.commit()
        return result
