from fastapi import FastAPI

from src.interfaces.auth import router_auth
from src.interfaces.todo import router_todo
from src.interfaces.task import router_task

app = FastAPI()

app.include_router(router_auth, prefix="/api/v1", tags=["users"])
app.include_router(router_todo, prefix="/api/v1", tags=["todo_lists"])
app.include_router(router_task, prefix="/api/v1", tags=["tasks"])
