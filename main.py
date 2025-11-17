from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

from tortoise import fields
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from models import TodoItem

app = FastAPI(title="TODO API", description="TODOリスト管理API", version="1.0.0")

# TortoiseモデルからPydanticモデルを自動生成: include=は必須、exclude=は除外
TodoItem_Pydantic = pydantic_model_creator(TodoItem)
TodoItemCreate_Pydantic = pydantic_model_creator(TodoItem, exclude=("id", "completed"))
TodoItemUpdate_Pydantic = pydantic_model_creator(TodoItem, exclude=("id",))

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models":["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)



class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoItemCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None

class TodoItemUpdateScheme(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


@app.get("/")
def read_root():
    return {"message": "TODO APIへようこそ！"}


@app.get("/todos", response_model=List[TodoItem_Pydantic])
async def get_all_todos():
    todos = await TodoItem.all()
    return todos



# 特定のTODOを取得
@app.get("/todos/{todo_id}", response_model=TodoItem_Pydantic)
async def get_todo(todo_id: int):
    todo = await TodoItem.get(id=todo_id)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail=f"ID {todo_id} のTODOが見つかりません")



@app.post("/todos", response_model=TodoItem_Pydantic)
async def create_todo(res: TodoItemCreate_Pydantic): # <--リクエストボディのデータを受け取る
    new_todo = await TodoItem.create(title=res.title, description=res.description)
    return new_todo # 追加したTODOアイテムを返す



@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    todo = await TodoItem.get(id=todo_id)
    if todo:
        await todo.delete()
        return {"message": f"TODO '{todo.title}' を削除しました"}
    raise HTTPException(status_code=404, detail=f"ID {todo_id} のTODOが見つかりません")



@app.put("/todos/{todo_id}", response_model=TodoItem_Pydantic)
def update_todo(todo_id: int, req: TodoItemUpdate_Pydantic):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[i] = TodoItem_Pydantic(
                id=todo_id,
                title=req.title if req.title is not None else todo.title,
                description=req.description if req.description is not None else todo.description,
                completed=req.completed if req.completed is not None else todo.completed
            )
            return todos[i]

    raise HTTPException(status_code=404, detail=f"ID {todo_id} のTODOが見つかりません")

    