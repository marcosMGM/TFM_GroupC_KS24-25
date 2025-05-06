from app.config import get_connection
import datetime

def get_datalist(params):

    """ select id, link, title, built_area, price
    FROM ide_property
    ORDER BY id ASC """


    limit = """ """
    select = """ """
    where = """ """
    group = """ """
    order = """ """
        

    data = [
        {"id": 1, "titulo": "Titulo 1"},
        {"id": 2, "titulo": "Titulo 2"},
        {"id": 3, "titulo": "Titulo 3"},
        {"id": 4, "titulo": "Titulo 4"},
        {"id": 5, "titulo": "Titulo 5"}
    ]

    # draw = int(request.args.get('draw', 1))
    # start = int(request.args.get('start', 0))
    # length = int(request.args.get('length', 10))
    # search_value = request.args.get('search[value]', '')

    return {
        "draw": int(params.get('draw', 1)),
        "recordsTotal": 5,
        "recordsFiltered": 4,
        "data": data
    }
















# def get_all_properties():
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT * FROM ide_property
#             WHERE login = ? AND estado = 1
#         """, (login,))
#         row = cursor.fetchone()
#         if row:
#             return User(id=row.id, login=row.login, password=row.password, nombre=row.nombre, apellidos=row.apellidos, email=row.email)
#         return None

# def update_last_access(user_id):
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute("UPDATE sys_user SET last_access = ? WHERE id = ?", (datetime.datetime.now(), user_id))
#         conn.commit()