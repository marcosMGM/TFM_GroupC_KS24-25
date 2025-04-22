from config import get_connection
import datetime

class User:
    def __init__(self, id, login, password, nombre):
        self.id = id
        self.login = login
        self.password = password
        self.nombre = nombre

def get_user_by_login(login):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, login, password, nombre
            FROM sys_user
            WHERE login = ? AND estado = 1
        """, (login,))
        row = cursor.fetchone()
        if row:
            return User(id=row.id, login=row.login, password=row.password, nombre=row.nombre)
        return None

def update_last_access(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE sys_user SET last_access = ? WHERE id = ?", (datetime.datetime.now(), user_id))
        conn.commit()
