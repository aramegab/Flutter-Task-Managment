from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    completed: bool = False

def init_db():
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL
            )
        """)
        conn.commit()

init_db()

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
            (task.title, task.description, task.completed)
        )
        task_id = cursor.lastrowid
        conn.commit()
        return {**task.dict(), "id": task_id}

@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, completed FROM tasks")
        tasks = [
            {"id": row[0], "title": row[1], "description": row[2], "completed": bool(row[3])}
            for row in cursor.fetchall()
        ]
        return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, completed FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"id": row[0], "title": row[1], "description": row[2], "completed": bool(row[3])}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        conn.commit()
        return {"message": "Task deleted"}

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
            (task.title, task.description, task.completed, task_id)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        conn.commit()
        return {**task.model_dump(), "id": task_id}