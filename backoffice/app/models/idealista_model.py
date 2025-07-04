from app.config import get_connection
from app.utils.database import DatabaseInterface
from app.models.custom_model import get_parameters_by_key
import datetime


def get_datalist(params, pagination=True):
    db = DatabaseInterface()

    """ SELECT BLOCK """
    select = """SELECT HOUSE_ID as id, URL as link, TITLE as title, BUILT_AREA as built_area, PRICE as price, DISTRITO, PRICE_PER_NIGHT, ARR, (FIXED_OPEX + VARIABLE_OPEX) as OPEX, ROI FROM HOUSES """


    """ FILTER BLOCK """
    where = """ WHERE 1=1 AND DISTRITO <> 'Not defined' """

    if params.get('ftr_district'):
        where += f" AND DISTRITO = '{params['ftr_district']}'"

    if params.get('ftr_text'):
        where += f" AND TITLE LIKE '%{params['ftr_text']}%'"

    min_price = params.get('ftr_buy_price_min')
    max_price = params.get('ftr_buy_price_max')
    try:
        if min_price is not None and min_price != '' and str(min_price).replace('.', '', 1).isdigit():
            where += f" AND PRICE >= {float(min_price)}"
        if max_price is not None and max_price != '' and str(max_price).replace('.', '', 1).isdigit():
            where += f" AND PRICE <= {float(max_price)}"
    except Exception:
        print(f"Error al procesar los filtros de precio: {min_price}, {max_price}")



    ##### SEARCH BOX #####
    filter_data = {
        'id' : 'HOUSE_ID',
        'title' : 'TITLE',
        'price' : 'PRICE',
        'built_area' : 'BUILT_AREA',
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
        order = " ORDER BY HOUSE_ID ASC"



    """ PAGINATION BLOCK  """
    limit = ""
    if pagination:
        if 'start' in params and str(params['length']) != '-1':
            limit += f" OFFSET {int(params['start'])} ROWS FETCH NEXT {int(params['length'])} ROWS ONLY"
        else:
            limit += f" FETCH NEXT {int(params['length'])} ROWS ONLY"



    results = db.getallfromquery(select + where + group + order + limit) if db.getallfromquery(select + where + group + order + limit) else []
    if results:
        parameters= get_parameters_by_key()
        estimated_anual_days_ocupation = int(round(int(parameters.get('ESTIMATED_ANNUAL_OCCUPANCY', {}).get('VALUE', 0)) /100 * 365,0))

        for result in results:
            result['revenue'] = result['PRICE_PER_NIGHT'] * estimated_anual_days_ocupation
            # print() 

    """ OUTPUT """
    # print(f"SELECT: {select + where + group + order + limit}")
    return {
        "draw": int(params.get('draw', 1)),
        "recordsTotal": db.getcountfromquery(select),
        "recordsFiltered": db.getcountfromquery(select + where),
        # "data": result if result else [],
        "data": results,
    }


def get_districts():
    db = DatabaseInterface()
    query = "SELECT DISTINCT DISTRITO FROM HOUSES WHERE DISTRITO <> 'Not defined' ORDER BY DISTRITO"
    return db.getallfromquery(query)


def get_min_price():
    db = DatabaseInterface()
    query = "SELECT MIN(PRICE) as min_price FROM HOUSES"
    result = db.getallfromquery(query)
    return result[0]['min_price'] if result else 0

def get_max_price():
    db = DatabaseInterface()
    query = "SELECT MAX(PRICE) as max_price FROM HOUSES"
    result = db.getallfromquery(query)
    return result[0]['max_price'] if result else 0












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