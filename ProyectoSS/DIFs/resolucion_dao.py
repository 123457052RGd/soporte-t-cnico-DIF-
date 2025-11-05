from db_manager import execute_query

class ResolucionDAO:
    def documentar_y_cerrar_ticket(self, id_ticket, diagnostico, solucion_aplicada, tiempo_empleado):
        """
        [ADMIN] Documenta la resolución del ticket y marca su estado como 'Resuelto'.

        Parámetros:
            id_ticket (int): ID del ticket a cerrar.
            diagnostico (str): Diagnóstico del técnico.
            solucion_aplicada (str): Descripción de la solución aplicada.
            tiempo_empleado (str): Tiempo total invertido en la resolución.

        Retorna:
            bool: True si ambas operaciones (insertar y actualizar) fueron exitosas, False si falló alguna.
        """
        try:
            # 1️⃣ Insertar la resolución
            sql_res = """
                INSERT INTO Resoluciones (id_ticket, diagnostico, solucion_aplicada, tiempo_empleado)
                VALUES (%s, %s, %s, %s)
            """
            params_res = (id_ticket, diagnostico, solucion_aplicada, tiempo_empleado)
            result_insert = execute_query(sql_res, params_res)

            if not result_insert:
                print(f"⚠️ Error al insertar la resolución para el ticket #{id_ticket}")
                return False

            # 2️⃣ Actualizar el estado del ticket
            sql_ticket = "UPDATE Tickets SET estado = 'Resuelto' WHERE id_ticket = %s"
            result_update = execute_query(sql_ticket, (id_ticket,))

            if not result_update:
                print(f"⚠️ Error al actualizar el estado del ticket #{id_ticket}")
                return False

            print(f"✅ Ticket #{id_ticket} documentado y cerrado correctamente.")
            return True

        except Exception as e:
            print(f"❌ Error en documentar_y_cerrar_ticket: {e}")
            return False
