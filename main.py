from fastapi import FastAPI, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database  # Импортируем наш файл с функциями работы с БД

app = FastAPI()



# Добавьте CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены. Можно заменить на список с доменами фронта, если нужно ограничить
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Разрешить все заголовки
)


# Модель для создания задачи без id
class TaskCreate(BaseModel):
    text: str
    completed: bool = False  # По умолчанию задача не завершена

# Модель для представления задачи с id (эта модель будет использоваться в ответах)
class Task(TaskCreate):
    id: int  # Добавляем id, который генерируется сервером

class UpdateTaskStatus(BaseModel):
    completed: bool



# Создаем таблицу в базе данных при запуске сервера
@app.on_event("startup")
async def startup():
    database.create_db()


# Эндпоинт для получения всех задач
@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    tasks = database.get_all_tasks()
    return [{"id": task[0], "text": task[1], "completed": bool(task[2])} for task in tasks]


# Эндпоинт для добавления новой задачи
@app.post("/tasks", response_model=Task)
async def add_task(task: TaskCreate):
    task_id = database.add_task(task.text)  # Генерация ID на сервере
    new_task = {"id": task_id, "text": task.text, "completed": task.completed}
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    # Проверяем, существует ли задача
    tasks = database.get_all_tasks()
    current_task = next((t for t in tasks if t[0] == task_id), None)
    if current_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Обновляем задачу в базе данных
    updated_task = database.update_task(task_id, task.text, task.completed)

    # Возвращаем обновлённую задачу
    return {
        "id": updated_task[0],
        "text": updated_task[1],
        "completed": bool(updated_task[2]),
    }



# Эндпоинт для удаления задачи
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    database.delete_task(task_id)
    return {"message": "Task deleted successfully"}