from app.config import get_connection
from app.utils.database import DatabaseInterface
from app.models.custom_model import get_parameters_by_key
import datetime


def get_datalist(params, pagination=True):
    db = DatabaseInterface()
    # print(f"Params received: {params}")

    """ SELECT BLOCK """
    select = """SELECT HOUSE_ID as id, URL as link, TITLE as title, BUILT_AREA as built_area, PRICE as price, 
    DISTRITO, PRICE_PER_NIGHT, ARR, (FIXED_OPEX + VARIABLE_OPEX) as OPEX, ROI, PER FROM HOUSES """


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


    min_roi = params.get('ftr_min_roi')
    try:
        if min_roi is not None and min_roi != '' and str(min_roi).replace('.', '', 1).isdigit():
            where += f" AND ROI >= {int(min_roi)}"
    except Exception:
        print(f"Error al procesar el filtro de ROI: {min_roi}")


  
    max_per = params.get('ftr_max_per')
    try:
        if max_per is not None and max_per != '' and float(max_per):
            where += f" AND (PER <= {float(max_per)} OR PER IS NULL)"
    except (ValueError, TypeError):
        print(f"Error al procesar el filtro de PER: {max_per}")
  
    roi_group = params.get('ftr_roi_group')
    try:
        if roi_group is not None and roi_group != '' and int(roi_group):
            roi_groups = get_percentile_roi()
            if roi_group == '1':
                where += f" AND ROI <= 0"
            elif roi_group == '2':
                where += f" AND ROI > 0 AND ROI <= {roi_groups['P33']}"
            elif roi_group == '3':
                where += f" AND ROI > {roi_groups['P33']} AND ROI <= {roi_groups['P66']}"
            elif roi_group == '4':
                where += f" AND ROI > {roi_groups['P66']} AND ROI <= {roi_groups['P90']}"
            elif roi_group == '5':
                where += f" AND ROI > {roi_groups['P90']}"
    except (ValueError, TypeError):
        print(f"Error al procesar el filtro de ROI_GROUP: {roi_group}")



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
    order = ""
    # Params received: ImmutableMultiDict([('draw', '3'), ('columns[0][data]', 'id'), ('columns[0][name]', ''), ('columns[0][searchable]', 'true'), ('columns[0][orderable]', 'true'), ('columns[0][search][value]', ''), ('columns[0][search][regex]', 'false'), ('columns[1][data]', 'DISTRITO'), ('columns[1][name]', ''), ('columns[1][searchable]', 'true'), ('columns[1][orderable]', 'true'), ('columns[1][search][value]', ''), ('columns[1][search][regex]', 'false'), ('columns[2][data]', 'title'), ('columns[2][name]', ''), ('columns[2][searchable]', 'true'), ('columns[2][orderable]', 'true'), ('columns[2][search][value]', ''), ('columns[2][search][regex]', 'false'), ('columns[3][data]', 'built_area'), ('columns[3][name]', ''), ('columns[3][searchable]', 'true'), ('columns[3][orderable]', 'true'), ('columns[3][search][value]', ''), ('columns[3][search][regex]', 'false'), ('columns[4][data]', 'link'), ('columns[4][name]', ''), ('columns[4][searchable]', 'true'), ('columns[4][orderable]', 'true'), ('columns[4][search][value]', ''), ('columns[4][search][regex]', 'false'), ('columns[5][data]', 'price'), ('columns[5][name]', ''), ('columns[5][searchable]', 'true'), ('columns[5][orderable]', 'true'), ('columns[5][search][value]', ''), ('columns[5][search][regex]', 'false'), ('columns[6][data]', 'PRICE_PER_NIGHT'), ('columns[6][name]', ''), ('columns[6][searchable]', 'true'), ('columns[6][orderable]', 'true'), ('columns[6][search][value]', ''), ('columns[6][search][regex]', 'false'), ('columns[7][data]', 'ARR'), ('columns[7][name]', ''), ('columns[7][searchable]', 'true'), ('columns[7][orderable]', 'true'), ('columns[7][search][value]', ''), ('columns[7][search][regex]', 'false'), ][search][value]', ''), ('columns[7][search][regex]', 'false'), ('columns[8][data]', 'OPEX'), ('columns[8][name]', ''), ('columns[8][searchable]', 'true'), ('columns[8][orderable]', 'true'), ('columns[8][search][value]', ''), ('columns[8][search][regex]', 'false'), ('columns[9][data]', 'ROI'), ('columns[9][name]', ''), ('columns[9][searchable]', 'true'), ('columns[9][orderable]', 'true'), ('columns[9][search][value]', ''), ('columns[9][search][regex]', 'false'), ('columns[10][data]', 'PER'), ('columns[10][name]', ''), ('columns[10][searchable]', 'true'), ('columns[10][orderable]', 'true'), ('columns[10][search][value]', ''), ('columns[10][search][regex]', 'false'), ('columns[11][data]', 'ROI'), ('columns[11][name]', ''), ('columns[11][searchable]', 'true'), ('columns[11][orderable]', 'true'), ('columns[11][search][value]', ''), ('columns[11][search][regex]', 'false'), ('order[0][column]', '0'), ('order[0][dir]', 'asc'), ('start', '0'), ('length', '10'), ('search[value]', ''), ('search[regex]', 'false'), ('ftr_text', ''), ('ftr_district', ''), ('ftr_buy_price_min', ''), ('ftr_buy_price_max', ''), ('ftr_min_roi', ''), ('ftr_max_per', '')])
    # print(f"Columna solicitada para ordenar: {params.get('order[0][column]')} cuyo nombre es: {params.get('columns[' + params.get('order[0][column]') + '][data]')}")
    if params.get('order[0][column]') and 'columns[0][data]' in params:
        """ añadir excepciones """
        """ si x columna, entonces x orden (fechas, etc) """
        order_column = params.get('columns['+ params.get('order[0][column]') +'][data]')
        sentido = params.get('order[0][dir]', 'ASC') #por omisión, ponemos ASC
        order = f" ORDER BY {order_column} {sentido}"

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


    """ OUTPUT """
    # print(f"SELECT: {select + where + group + order + limit}")
    return {
        "draw": int(params.get('draw', 1)),
        "recordsTotal": db.getcountfromquery(select + " WHERE 1=1 AND DISTRITO <> 'Not defined' "),
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

def get_max_roi():
    db = DatabaseInterface()
    query = "SELECT MAX(ROI) as max_roi FROM HOUSES"
    result = db.getallfromquery(query)
    return result[0]['max_roi'] if result else 0

def get_min_roi():
    db = DatabaseInterface()
    query = "SELECT MIN(ROI) as min_roi FROM HOUSES"
    result = db.getallfromquery(query)
    return result[0]['min_roi'] if result else 0

def get_percentile_roi():
    db = DatabaseInterface()
    query = """
    SELECT TOP 1
        PERCENTILE_CONT(0.33) WITHIN GROUP (ORDER BY ROI) OVER () AS P33,
        PERCENTILE_CONT(0.66) WITHIN GROUP (ORDER BY ROI) OVER () AS P66,
        PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY ROI) OVER () AS P90
    FROM (
        SELECT ROI FROM HOUSES WHERE ROI > 0
    ) AS subquery;
    """
    result = db.getallfromquery(query)
    return result[0] if result else {'P33': 0, 'P66': 0, 'P90': 0}
















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