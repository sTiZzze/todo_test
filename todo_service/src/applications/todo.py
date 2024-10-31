from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from src.infrastructure.repositories.todo import TodoListRepository


class TodoService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.__session = TodoListRepository(session)

    async def get_todo(self, entity, user):
        return await self.__session.get_all(entity, user)

    async def create_todo(self, entity, model, user):
        return await self.__session.create(entity, model, user)

    async def update_todo(self, entity, model, user, id):
        return await self.__session.update(entity, model, user, id)
