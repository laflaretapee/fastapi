import sqlite3

# Функция для создания таблицы в базе данных
def create_db():
    conn = sqlite3.connect('tasks.db')  # Подключение к базе данных (или её создание)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()

# Функция для получения всех задач
def get_all_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Функция для добавления новой задачи
def add_task(text: str):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (text, completed) VALUES (?, ?)', (text, False))
    conn.commit()
    task_id = cursor.lastrowid  # Получаем сгенерированный id
    conn.close()
    return task_id

def update_task(self, task_id, text, completed):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Обновляем поля задачи в базе данных
    cursor.execute(
        "UPDATE tasks SET text = ?, completed = ? WHERE id = ?",
        (text, completed, task_id)
    )
    conn.commit()

    # Извлекаем обновлённую задачу
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    updated_task = cursor.fetchone()

    conn.close()
    if updated_task:
        return updated_task
    else:
        return None



# Функция для удаления задачи
def delete_task(id: int):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
