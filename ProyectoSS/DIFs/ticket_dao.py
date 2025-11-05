from db_manager import execute_query

class TicketDAO:
    def crear_ticket(self, id_cliente, id_activo, asunto, descripcion_problema):
        """[CLIENTE] Crea un ticket con estado 'Abierto'."""
        sql = """
        INSERT INTO Tickets 
        (id_cliente, id_activo, asunto, descripcion_problema) 
        VALUES (%s, %s, %s, %s)
        """
        params = (id_cliente, id_activo, asunto, descripcion_problema)
        return execute_query(sql, params)

    def obtener_tickets_pendientes_admin(self):
        """[ADMIN] Lista TODOS los tickets (incluyendo Resueltos/Historial)."""
        sql = """
        SELECT 
            T.id_ticket, T.asunto, T.estado, T.prioridad, T.id_activo,
            C.nombre AS nombre_cliente, C.apellido AS apellido_cliente, C.departamento,
            A.serial_number, A.ubicacion, A.numero_inventario,
            TE.nombre AS nombre_responsable, TE.apellido AS apellido_responsable
        FROM 
            Tickets T
        JOIN Clientes C ON T.id_cliente = C.id_cliente
        JOIN Activos A ON T.id_activo = A.id_activo
        LEFT JOIN Tecnicos TE ON T.id_tecnico = TE.id_tecnico
        -- Consulta sin WHERE para mostrar todos los estados como historial
        ORDER BY 
            T.estado ASC, T.fecha_apertura DESC 
        """
        return execute_query(sql, fetch=True)
    
    def asignar_tecnico(self, id_ticket, id_tecnico):
        """[ADMIN] Asigna un ticket y cambia el estado a 'En Progreso'."""
        sql = "UPDATE Tickets SET id_tecnico = %s, estado = 'En Progreso' WHERE id_ticket = %s AND estado = 'Abierto'"
        execute_query(sql, (id_tecnico, id_ticket))

    def obtener_detalles_historial(self, id_ticket):
        """[ADMIN] Obtiene todos los datos para la documentación final."""
        sql = """
        SELECT 
            T.id_ticket, T.estado,
            C.nombre AS nombre_cliente, C.apellido AS apellido_cliente, 
            A.ubicacion, A.serial_number AS NS, A.numero_inventario AS No_Inventario,
            TE.nombre AS nombre_tecnico, TE.apellido AS apellido_tecnico
        FROM 
            Tickets T
        JOIN Clientes C ON T.id_cliente = C.id_cliente
        JOIN Activos A ON T.id_activo = A.id_activo
        LEFT JOIN Tecnicos TE ON T.id_tecnico = TE.id_tecnico
        WHERE 
            T.id_ticket = %s
        """
        return execute_query(sql, (id_ticket,), fetch=True)