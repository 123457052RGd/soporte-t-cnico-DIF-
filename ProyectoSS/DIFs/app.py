from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from cliente_dao import ClienteDAO
from tecnico_dao import TecnicoDAO
from activo_dao import ActivoDAO
from ticket_dao import TicketDAO
from resolucion_dao import ResolucionDAO


app = Flask(__name__)
app.secret_key = 'clave_secreta_del_sistema'

# Inicializamos las DAOs
cliente_dao = ClienteDAO()
tecnico_dao = TecnicoDAO()
activo_dao = ActivoDAO()
ticket_dao = TicketDAO()
resolucion_dao = ResolucionDAO()

# --- Definición de PROBLEMAS COMUNES y Consejos (ITIL Zero-Level) ---
PROBLEMAS_COMUNES = {
    'Internet/Red': {
        'opciones': ['Lentitud de conexión', 'No hay conexión (Cable desconectado)', 'No reconoce el WiFi', 'Otra'],
        'consejo': 'Por favor, verifique que el cable de red esté conectado correctamente y reinicie su equipo. Si el problema persiste, envíe el ticket.'
    },
    'Impresora': {
        'opciones': ['No imprime', 'No hay tinta/tóner', 'Atasco de papel', 'Otra'],
        'consejo': 'Verifique si la impresora tiene papel o si el indicador de tinta/tóner está encendido. Si el problema no es físico (falta de insumos), envíe el ticket.'
    },
    'Computadora': {
        'opciones': ['Equipo lento', 'Falla al iniciar (pantalla negra)', 'Programa no funciona', 'Otra'],
        'consejo': 'Intente cerrar los programas que no está usando y libere espacio en el escritorio. Si el equipo no enciende, proceda a enviar el ticket.'
    }
}


# --- DECORADOR DE AUTENTICACIÓN ---
def login_required(role=None):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not session.get('logged_in'):
                flash('Debe iniciar sesión para acceder.', 'warning')
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                flash(f'Acceso denegado. Se requiere el rol: {role}.', 'danger')
                return redirect(url_for('index'))
            return func(*args, **kwargs)
        return decorated_view
    return wrapper

# --- RUTAS DE ACCESO ---
@app.route('/')
def index():
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    if session.get('role') == 'cliente':
        return redirect(url_for('reportar_incidente'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        tecnico = tecnico_dao.autenticar(email, password)
        if tecnico:
            session['logged_in'] = True
            session['user_id'] = tecnico['id_tecnico']
            session['role'] = 'admin'
            flash('Bienvenido, Administrador.', 'success')
            return redirect(url_for('admin_dashboard'))

        cliente = cliente_dao.autenticar(email, password)
        if cliente:
            session['logged_in'] = True
            session['user_id'] = cliente['id_cliente']
            session['role'] = 'cliente'
            flash('Bienvenido, Trabajador.', 'success')
            return redirect(url_for('reportar_incidente'))
        
        flash('Credenciales incorrectas.', 'danger')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('login'))

# --- RUTA CLIENTE: REPORTAR INCIDENTE (Corregido el NameError) ---
@app.route('/reportar', methods=['GET', 'POST'])
@login_required(role='cliente') 
def reportar_incidente():
    id_cliente = session['user_id'] 
    
    activos_asignados = activo_dao.obtener_activos_por_cliente(id_cliente)
    
    if request.method == 'POST':
        id_activo = request.form['id_activo']
        asunto = request.form['asunto']
        # Eliminamos la obtención de 'descripcion_problema' del formulario
        descripcion = "" # Se pasa cadena vacía, ya que el detalle va en 'asunto'
        
        # Validar que el asunto no esté vacío (seguridad)
        if not asunto:
            flash("Error: Debe seleccionar y describir el problema.", 'danger')
            return redirect(url_for('reportar_incidente'))
        
        ticket_id = ticket_dao.crear_ticket(id_cliente, id_activo, asunto, descripcion) # Usamos la variable 'descripcion' vacía
        
        if ticket_id:
            flash(f"Incidente reportado exitosamente. Su número de ticket es: #{ticket_id}", 'success')
            return redirect(url_for('reportar_incidente'))
        else:
            flash("Error al crear el ticket en la base de datos.", 'danger')

    return render_template('cliente_reportar.html',
                        activos=activos_asignados,
                        problemas_comunes=PROBLEMAS_COMUNES)


# --- RUTAS ADMINISTRADOR ---
@app.route('/admin')
@login_required(role='admin')
def admin_dashboard():
    # Obtiene todos los tickets (pendientes y resueltos)
    tickets = ticket_dao.obtener_tickets_pendientes_admin() 
    
    # Obtener lista simple de técnicos para la asignación
    tecnicos = [{'id_tecnico': 1, 'nombre': 'Ana Gomez'}] 
    
    return render_template('admin_dashboard.html', tickets=tickets, tecnicos=tecnicos)


@app.route('/admin/asignar/<int:id_ticket>', methods=['POST'])
@login_required(role='admin')
def asignar_ticket(id_ticket):
    id_tecnico = request.form['id_tecnico']
    ticket_dao.asignar_tecnico(id_ticket, id_tecnico)
    
    flash(f"Ticket #{id_ticket} asignado.", 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/cerrar/<int:id_ticket>', methods=['GET', 'POST'])
@login_required(role='admin')
def cerrar_ticket(id_ticket):
    ticket_info = ticket_dao.obtener_detalles_historial(id_ticket)
    
    if not ticket_info or ticket_info[0]['estado'] == 'Resuelto':
        flash("Ticket no encontrado o ya resuelto.", 'warning')
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        diagnostico = request.form['diagnostico']
        solucion_aplicada = request.form['solucion_aplicada']
        tiempo_empleado = request.form['tiempo_empleado']

        resolucion_dao.documentar_y_cerrar_ticket(id_ticket, diagnostico, solucion_aplicada, tiempo_empleado)
        
        flash(f"Servicio del Ticket #{id_ticket} documentado y RESUELTO.", 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_cerrar.html', ticket=ticket_info[0])

@app.route('/admin/historial_activo/<int:id_activo>')
@login_required(role='admin')
def historial_activo(id_activo):
    # 1. Obtener la información del Activo (Siempre necesaria para el encabezado)
    activo_info = activo_dao.obtener_activo_por_id(id_activo)
    
    if not activo_info:
        flash("Error: El Activo (máquina) no se encontró en la base de datos.", 'danger')
        return redirect(url_for('admin_dashboard'))
        
    # 2. Obtener el historial de resoluciones
    historial = activo_dao.obtener_historial_por_activo(id_activo)

    if not historial:
        flash(f"No hay historial de soporte registrado para el activo con N/S: {activo_info[0]['serial_number']}.", 'info')
        
    return render_template('admin_historial_activo.html',
                        historial=historial,
                        activo_id=id_activo,
                        activo_info=activo_info[0])


if __name__ == '__main__':
    app.run(debug=True)