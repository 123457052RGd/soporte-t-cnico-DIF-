from db_manager import execute_query

class ClienteDAO:
    """
    Clase encargada de manejar las operaciones relacionadas con los clientes
    dentro del sistema (autenticación, obtención de datos, etc.)
    """

    def autenticar(self, email, password):
        """
        Verifica si un cliente existe en la base de datos con el correo y contraseña proporcionados.
        Retorna un diccionario con los datos del cliente si la autenticación es exitosa.
        De lo contrario, retorna None.
        """
        try:
            sql = """
                SELECT id_cliente, nombre
                FROM Clientes
                WHERE email = %s AND password = %s
            """
            result = execute_query(sql, (email, password), fetch=True)

            # Devuelve el primer registro si existe
            return result[0] if result else None

        except Exception as e:
            print(f"Error en ClienteDAO.autenticar: {e}")
            return None


    def obtener_todos(self):
        """
        Devuelve una lista con todos los clientes registrados en la base de datos.
        """
        try:
            sql = "SELECT id_cliente, nombre, email FROM Clientes"
            result = execute_query(sql, fetch=True)
            return result if result else []

        except Exception as e:
            print(f"Error en ClienteDAO.obtener_todos: {e}")
            return []


    def obtener_por_id(self, id_cliente):
        """
        Devuelve la información de un cliente específico por su ID.
        """
        try:
            sql = """
                SELECT id_cliente, nombre, email
                FROM Clientes
                WHERE id_cliente = %s
            """
            result = execute_query(sql, (id_cliente,), fetch=True)
            return result[0] if result else None

        except Exception as e:
            print(f"Error en ClienteDAO.obtener_por_id: {e}")
            return None
