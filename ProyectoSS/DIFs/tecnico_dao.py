from db_manager import execute_query
import bcrypt

class TecnicoDAO:
    def autenticar(self, email, password_ingresada):
        # 1. Consulta para obtener el hash de la contraseña y los datos.
        # Asegúrate de que la columna de la contraseña se llame 'password_hash'
        sql_fetch = "SELECT id_tecnico, nombre, password_hash FROM Tecnicos WHERE email = %s" 
        result = execute_query(sql_fetch, (email,), fetch=True)
        
        if result:
            tecnico_data = result[0]
            stored_hash = tecnico_data['password_hash']
            
            # 2. Verifica la contraseña ingresada contra el hash almacenado (¡MANDATORIO!)
            # Reemplaza 'verificar_password' por tu librería real (ej: bcrypt.checkpw)
            if verificar_password(password_ingresada, stored_hash): 
                # Eliminar el hash antes de devolver los datos del usuario
                del tecnico_data['password_hash']
                return tecnico_data 
            
        return None
def verificar_password(password_ingresada, stored_hash):
    return bcrypt.checkpw(password_ingresada.encode('utf-8'), stored_hash.encode('utf-8'))

