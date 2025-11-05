from db_manager import execute_query

class ActivoDAO:
    def obtener_activos_por_cliente(self, id_cliente):
        """Obtiene las máquinas asignadas a un cliente específico."""
        sql = "SELECT id_activo, tipo_activo, serial_number FROM Activos WHERE id_cliente = %s"
        return execute_query(sql, (id_cliente,), fetch=True)

    def obtener_activo_por_id(self, id_activo):
        """Obtiene la información básica de un activo por su ID, para el encabezado del historial."""
        sql = "SELECT serial_number, numero_inventario, tipo_activo, ubicacion FROM Activos WHERE id_activo = %s"
        return execute_query(sql, (id_activo,), fetch=True)

    def obtener_historial_por_activo(self, id_activo):
        """Obtiene el historial completo de resoluciones para un activo específico."""
        sql = """
        SELECT
            R.fecha_resolucion, R.diagnostico, R.solucion_aplicada, R.tiempo_empleado,
            T.id_ticket, T.asunto,
            TE.nombre AS responsable_nombre, TE.apellido AS responsable_apellido
        FROM
            Resoluciones R
        JOIN Tickets T ON R.id_ticket = T.id_ticket
        LEFT JOIN Tecnicos TE ON T.id_tecnico = TE.id_tecnico
        WHERE
            T.id_activo = %s
        ORDER BY
            R.fecha_resolucion DESC
        """
        return execute_query(sql, (id_activo,), fetch=True)