from db_manager import execute_query

class ResolucionDAO:
    def obtener_todas(self):
        sql = "SELECT * FROM Resoluciones"
        return execute_query(sql, fetch=True)

    def agregar(self, descripcion, estado):
        sql = "INSERT INTO Resoluciones (descripcion, estado) VALUES (%s, %s)"
        execute_query(sql, (descripcion, estado))