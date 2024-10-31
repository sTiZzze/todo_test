from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from src.infrastructure.repositories.task import TaskRepository


class TaskService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.__session = TaskRepository(session)

    async def get_task(self, entity, user):
        return await self.__session.get_all(entity, user)

    async def create_task(self, entity, model, user):
        return await self.__session.create(entity, model, user)

    async def update_task(self, entity, model, user, id):
        return await self.__session.update(entity, model, user, id)

    async def get_task_by_id(self, entity, user, id: int):
        return await self.__session.get_by_id(entity, user, id)
