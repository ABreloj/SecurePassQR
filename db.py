from flask import Flask, render_template, request, redirect, session, make_response, url_for
from functools import wraps
from flask_login import LoginManager, UserMixin, login_required, login_user

import pymongo

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

login_manager = LoginManager(app)
login_manager.login_view = 'iniciar_sesion'

def get_connection():
    return pymongo.MongoClient("mongodb://localhost:27017/")

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

def Inicio_Requerido(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        if not session.get('Usuario'):
            # Capturar la URL a la que intentaron acceder
            session['next_url'] = request.url
            return redirect(url_for('iniciar_sesion'))
        return view_func(*args, **kwargs)
    return decorated_function

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    mensaje = None

    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        
        # Crear una conexión a la base de datos
        connection = get_connection()

        # Seleccionar la colección de alumnos
        mi_base_de_datos = connection["SecurePassQR"]
        mi_coleccion = mi_base_de_datos["Alumnos"]

        # Consultar la colección para verificar el usuario y la contraseña
        usuario_encontrado = mi_coleccion.find_one({"Usuario": usuario, "Contraseña": contrasena})

        connection.close()

        if usuario_encontrado is None:
            # Usuario no registrado o contraseña incorrecta uwu
            mensaje = 'Usuario no registrado o contraseña incorrecta'
        else:
            # Convertir ObjectId a cadena
            usuario_encontrado['_id'] = str(usuario_encontrado['_id'])

            user = User()
            user.id = usuario_encontrado['_id']

            login_user(user)
            session['Usuario'] = usuario_encontrado

            # Redirigir a la URL capturada o al visualizar si no hay URL capturada
            next_url = session.pop('next_url', None)
            response = make_response(redirect(next_url or '/visualizar'))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            return response

    return render_template('iniciar_sesion.html', mensaje=mensaje)

@app.route('/visualizar')
@Inicio_Requerido
def visualizar():
    usuario_actual = session['Usuario']

    # Crear una conexión a la base de datos
    connection = get_connection()

    # Seleccionar la colección de alumnos
    mi_base_de_datos = connection["SecurePassQR"]
    mi_coleccion = mi_base_de_datos["Alumnos"]

    # Consultar la colección para obtener los datos de los estudiantes
    datos_estudiantes = list(mi_coleccion.find({}, {'_id': 0}))

    # Convertir ObjectId a cadena en cada documento
    for estudiante in datos_estudiantes:
        estudiante['Matricula'] = str(estudiante['Matricula'])

    connection.close()

    return render_template('visualizacion.html', usuario=usuario_actual, datos_estudiantes=datos_estudiantes)

@app.route('/registrar', methods=['GET', 'POST'])
@Inicio_Requerido
def registrar():
    usuario_actual = session['Usuario']

    if request.method == 'POST':
        matricula = request.form['matricula']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        carrera = request.form['carrera']
        usuario = request.form['usuario']

        contraseña = request.form['contraseña']

        connection = get_connection()

        mi_base_de_datos = connection["SecurePassQR"]
        mi_coleccion = mi_base_de_datos["Alumnos"]

        nuevo_estudiante = {
            "Matricula": matricula,
            "Nombre": nombre,
            "Apellidos": apellidos,
            "Carrera": carrera,
            "Usuario": usuario,
            "Contraseña": contraseña
        }

        mi_coleccion.insert_one(nuevo_estudiante)

        connection.close()

        return redirect('/visualizar')

    return render_template('registrar.html', usuario=usuario_actual)

@app.route('/about')
def about():

    return render_template('About.html')

if __name__ == "__main__":
    app.run(debug=True)
