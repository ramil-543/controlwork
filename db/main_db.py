import sqlite3

class ToDoDB:
    def __init__(self, db_name="todo.db"):
        self.db_name = db_name
        self.conn = None

    def init_db(self):
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def get_tasks(self, filter_type='all'):
        cursor = self.conn.cursor()
        if filter_type == 'completed':
            cursor.execute("SELECT id, task, completed FROM tasks WHERE completed = 1")
        elif filter_type == 'uncompleted':
            cursor.execute("SELECT id, task, completed FROM tasks WHERE completed = 0")
        else:
            cursor.execute("SELECT id, task, completed FROM tasks")
        return cursor.fetchall()

    def add_task(self, task):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        self.conn.commit()
        return cursor.lastrowid

    def update_task(self, task_id, new_task=None, completed=None):
        cursor = self.conn.cursor()
        if new_task is not None:
            cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
        if completed is not None:
            cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
        self.conn.commit()

    # НАШ ОБОРОТ ДЛЯ ЗАДАНИЯ 2: Удаление задачи
    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

main_db = ToDoDB()