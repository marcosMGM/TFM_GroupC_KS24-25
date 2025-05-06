from app.config import get_connection
import datetime


def get_all_properties():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM ide_property
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