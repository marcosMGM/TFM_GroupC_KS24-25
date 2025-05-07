from app.config import get_connection
from app.utils.database import db
import datetime

def get_datalist(params):

    top = f"TOP {int(params['length'])}"
    select = """SELECT {top} id, link, title, built_area, price FROM ide_property WHERE 1=1"""
    where = """ """
    group = """ """
    order = """ """
    query = select.format(top=top) + where + group + order
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

        # For recordsTotal and recordsFiltered, you'd typically run separate count queries
        # For simplicity, using len(data) for now, but this is not accurate if pagination/filtering is applied server-side.

        records_total = len(data) # This should be a COUNT(*) query without filters
        records_filtered = len(data) # This should be a COUNT(*) query with filters

    # data = [
    #     {"id": 1, "titulo": "Titulo 1"},
    #     {"id": 2, "titulo": "Titulo 2"},
    #     {"id": 3, "titulo": "Titulo 3"},
    #     {"id": 4, "titulo": "Titulo 4"},
    #     {"id": 5, "titulo": "Titulo 5"}
    # ]

    # draw = int(request.args.get('draw', 1))
    # start = int(request.args.get('start', 0))
    # length = int(request.args.get('length', 10))
    # search_value = request.args.get('search[value]', '')

    return {
        "draw": int(params.get('draw', 1)),
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
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