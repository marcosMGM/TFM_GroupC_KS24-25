from app.config import get_connection
from app.utils.database import DatabaseInterface
import datetime


def get_datalist(params, pagination=True):
    db = DatabaseInterface()

    """ SELECT BLOCK """
    select = """SELECT id, link, title, built_area, price FROM ide_property """


    """ FILTER BLOCK """
    where = """ WHERE 1=1 """

    ##### SEARCH BOX #####
    filter_data = {
        'id' : 'id',
        'title' : 'title',
        'price' : 'price',
        'built_area' : 'built_area',
    }
    search = params.get('search[value]', '').lower()
    sqlWhere = ''
    columns = []
    # reconstruir columnas. TODO empaquetar en una función en UTILS
    i = 0
    while True:
        col_data = params.get(f'columns[{i}][data]')
        if col_data is None:
            break
        columns.append({
            'data': col_data,
            'searchable': params.get(f'columns[{i}][searchable]'),
            'search_value': params.get(f'columns[{i}][search][value]'),
        })
        i += 1

    for col in columns:
        if col['searchable'] == 'true' and col['data'] in filter_data:
            if search:
                sqlWhere += f" OR LOWER({filter_data[col['data']]}) LIKE '%{search}%'"
                print(f"Añadiendo filtro: {col['data']} -> {filter_data[col['data']]}")
            elif col['search_value']:
                value = col['search_value'].lower()
                sqlWhere += f" OR LOWER({filter_data[col['data']]}) LIKE '%{value}%'"
                print(f"Añadiendo filtro por columna: {col['data']}")

    if sqlWhere.strip():
        where += " AND (" + sqlWhere.lstrip(" OR") + ")"


    """ GROUP BLOCK """
    group = """ """


    """ ORDER BLOCK """
    if params.get('order') and len(params['order']) > 0 and 'columns' in params:
        orderColumns = []

        for i in range(len(params['order'])):
            columnIdx = int(params['order'][i].get('column', 0))
            requestColumn = params['columns'][columnIdx]

            if requestColumn.get('orderable') == 'true':
                dir = 'ASC' if params['order'][i].get('dir') == 'asc' else 'DESC'

                if requestColumn.get('data') == 'activa':
                    orderColumns.append(f"p.activa {dir}")
                else:
                    orderColumns.append(f"{requestColumn.get('data')} {dir}")

        if orderColumns:
            order = " ORDER BY " + ", ".join(orderColumns)
    #Orden por omisión
    if 'order' not in locals() or not order:
        order = " ORDER BY id ASC"



    """ PAGINATION BLOCK  """
    limit = ""
    if pagination:
        if 'start' in params and str(params['length']) != '-1':
            limit += f" OFFSET {int(params['start'])} ROWS FETCH NEXT {int(params['length'])} ROWS ONLY"
        else:
            limit += f" FETCH NEXT {int(params['length'])} ROWS ONLY"


    """ OUTPUT """
    # print(f"SELECT: {select + where + group + order + limit}")
    return {
        "draw": int(params.get('draw', 1)),
        "recordsTotal": db.getcountfromquery(select),
        "recordsFiltered": db.getcountfromquery(select + where),
        # "data": result if result else [],
        "data": db.getallfromquery(select + where + group + order + limit) if db.getallfromquery(select + where + group + order + limit) else [],
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