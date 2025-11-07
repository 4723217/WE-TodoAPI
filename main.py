from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="TODO API", description="TODOリスト管理API", version="1.0.0")

class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

todos = [
    TodoItem(id=1, title="牛乳とパンを買う", description="牛乳は低温殺菌じゃないとだめ", completed=False),
    TodoItem(id=2, title="Pythonの勉強", description="30分勉強する", completed=True),
    TodoItem(id=3, title="30分のジョギング", description="", completed=False),
    TodoItem(id=4, title="技術書を読む", description="", completed=False),
    TodoItem(id=5, title="夕食の準備", description="カレーを作る", completed=True)
]

@app.get("/")
def read_root():
    return {"message": "TODO APIへようこそ！"}


@app.get("/todos", response_model=List[TodoItem])
def get_all_todos(query: Optional[str]=None):
    if query:
        results: List[TodoItem] = [] 
        for todo in todos: 
            if query.lower() in todo.title or query.lower() in todo.description: 
                results.append(todo)
        return results
    else:
        return todos


# 特定のTODOを取得
@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="TODOが見つからない")
