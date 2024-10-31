from typing import List

from sqlalchemy import Boolean, ForeignKey, Integer, String, text, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base
from src.domain.models.abstract_models import AbstractModel
from src.domain.models.user import User


class TodoList(AbstractModel):
    __tablename__ = 'todo_list'
    __mapper_args__ = {"concrete": True}
    __table_args__ = {"postgresql_inherits": AbstractModel.__table__.name}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String,  nullable=False)
    completed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default='False')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    user: Mapped["User"] = relationship()
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="todo_list")


class Task(AbstractModel):
    __tablename__ = 'task'
    __mapper_args__ = {"concrete": True}
    __table_args__ = {"postgresql_inherits": AbstractModel.__tablename__}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String,  nullable=False)
    task_info: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(
        ENUM('in_progress', 'done', name='status_task'),
        nullable=False,
        server_default=text("'in_progress'")
        )
    datetime_to_do = mapped_column(DateTime(timezone=True))
    todo_list_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'todo_list.id', ondelete='CASCADE'), nullable=False)
    todo_list: Mapped["TodoList"] = relationship("TodoList", back_populates="tasks")
