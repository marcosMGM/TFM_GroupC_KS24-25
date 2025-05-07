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
    if params.get('search') and params['search'].get('value', '') != '':
        filter_data = {
            'id' : 'id',
            'title' : 'title'
        }
        sqlWhere = ""
        search = params['search']['value'].lower().replace("'", "''")  # escapado simple para LIKE
        for i in range(len(params['columns'])):
            requestColumn = params['columns'][i]
            if requestColumn.get('searchable') == 'true' and requestColumn['data'] in filter_data:
                sqlWhere += f" OR LOWER({filter_data[requestColumn['data']]}) LIKE '%{search}%'"
                print(sqlWhere)
                # A ESTE PRINT NO ESTA ENTRANDO REVISAR
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
    print(f"SELECT: {select + where + group + order + limit}")
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