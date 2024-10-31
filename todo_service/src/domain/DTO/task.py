from datetime import datetime
from typing import List

from pydantic import BaseModel, constr


class TaskBase(BaseModel):
    id: int
    title: constr(max_length=50)
    task_info: constr(max_length=256)
    todo_list_id: int
    status: str = 'in_progress' or 'done'
    datetime_to_do: datetime

    class Config:
        from_attributes = True


class TaskCreateUpdate(BaseModel):
    title: constr(max_length=50)
    task_info: constr(max_length=256)
    todo_list_id: int
    datetime_to_do: datetime

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: constr(max_length=50)
    task_info: constr(max_length=256)
    todo_list_id: int
    status: str = 'in_progress' or 'done'
    updated_at: datetime = datetime.now()
    datetime_to_do: datetime

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    tasks: List[TaskBase]


class TodoListBase(BaseModel):
    id: int
    title: constr(max_length=50)
    completed: bool
    tasks: List[TaskBase]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TodoListCreateUpdate(BaseModel):
    title: constr(max_length=50)
    completed: bool
    user_id: int

    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    tasks: List[TodoListBase]
