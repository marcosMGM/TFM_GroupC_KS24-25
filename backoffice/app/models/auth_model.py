
from app.config import get_connection
import datetime
from werkzeug.security import generate_password_hash

class User:
    def __init__(self, id, login, password, nombre, apellidos, email):
        self.id = id
        self.login = login
        self.password = password
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email

def get_user_by_login(login):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, login, password, nombre, apellidos, email
            FROM sys_user
            WHERE login = ? AND estado = 1
        """, (login,))
        row = cursor.fetchone()
        if row:
            return User(id=row.id, login=row.login, password=row.password, nombre=row.nombre, apellidos=row.apellidos, email=row.email)
        return None

def update_last_access(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE sys_user SET last_access = ? WHERE id = ?", (datetime.datetime.now(), user_id))
        conn.commit()

def update_password(user_id, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE sys_user SET password = ? WHERE id = ?", (generate_password_hash(password), user_id))
        conn.commit()
