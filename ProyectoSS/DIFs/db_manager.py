import mysql.connector
from mysql.connector import Error

# Configuración de la base de datos
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '558902',
    'database': 'DIFSof'
}

def get_connection():
    """
    Establece y devuelve una conexión a la base de datos MySQL.
    Retorna el objeto de conexión si se establece correctamente, 
    o None si ocurre un error.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
        else:
            print("No se pudo establecer la conexión con la base de datos.")
            return None
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None


def execute_query(sql, params=None, fetch=False):
    """
    Ejecuta una consulta SQL en la base de datos.

    Parámetros:
        sql (str): Sentencia SQL a ejecutar.
        params (tuple | None): Parámetros para la consulta.
        fetch (bool): Si es True, devuelve los resultados de la consulta (SELECT).

    Retorna:
        - Si fetch=True → lista de diccionarios con los resultados.
        - Si fetch=False → ID del último registro insertado o True si no aplica.
        - None en caso de error.
    """
    conn = get_connection()
    if conn is None:
        print("⚠️ No hay conexión con la base de datos.")
        return None

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())

        if fetch:
            result = cursor.fetchall()
            return result if result else []

        conn.commit()
        return cursor.lastrowid if cursor.lastrowid else True

    except Error as e:
        print(f"❌ Error al ejecutar la consulta: {e}\nSQL: {sql}\nParámetros: {params}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
