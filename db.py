from flask import Flask, render_template, request, redirect, session, url_for
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Inicializar la aplicación de Firebase
cred = credentials.Certificate('passqr-9141c-firebase-adminsdk-ahwbs-2c35df3e92.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/crear_usuarios', methods=['GET'])
def crear_usuarios():
    # Lista de usuarios con sus datos
    usuarios_nuevos = [
        {
            'Matricula': '2022IDGS030',
            'Nombre': 'Santiago',
            'Apellidos': 'Montiel Sosa',
            'Carrera': 'TIADSM',
            'Usuario': 'SantiagoIDGS030',
            'Contraseña': 'TIADSM030',
            'Salida': '',
            'Entrada': '',
        },
        {
            'Matricula': '2022IDGS009',
            'Nombre': 'Juan Manuel',
            'Apellidos': 'Hernández Sánchez',
            'Carrera': 'TIADSM',
            'Usuario': 'JuanIDGS009',
            'Contraseña': 'TIADSM009',
            'Salida': '',
            'Entrada': '',
        },
        {
            'Matricula': '20221DGS059',
            'Nombre': 'Andoni Agustín',
            'Apellidos': 'López Sandoval',
            'Carrera': 'TIADSM',
            'Usuario': 'AndoniIDGS059',
            'Contraseña': 'TIADSM059',
            'Salida': '',
            'Entrada': '',
        },
        {
            'Matricula': '2022IDGS071',
            'Nombre': 'Alvaro',
            'Apellidos': 'Aguirre Palestina',
            'Carrera': 'TIADSM',
            'Usuario': 'AlvaroIDGS071',
            'Contraseña': 'TIADSM071',
            'Salida': '',
            'Entrada': '',
        },
    ]

    # Obtener una referencia a la colección 'usuarios' en Firestore
    usuarios_ref = db.collection('usuarios')

    # Agregar cada usuario a la colección 'usuarios'
    for usuario in usuarios_nuevos:
        usuarios_ref.add(usuario)

    return 'Usuarios creados correctamente'

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        # Consultar Firebase para verificar el usuario y la contraseña
        usuarios_ref = db.collection('usuarios')
        query = usuarios_ref.where('Usuario', '==', usuario).where('Contraseña', '==', contrasena).limit(1)
        results = query.get()

        if len(results) == 0:
            # Usuario no registrado o contraseña incorrecta
            mensaje = 'Usuario no registrado o contraseña incorrecta'
            return render_template('iniciar_sesion.html', mensaje=mensaje)

        usuario_encontrado = results[0].to_dict()

        session['user'] = usuario_encontrado
        return redirect('/visualizar')

    return render_template('iniciar_sesion.html')

@app.route('/visualizar')
def visualizar():
    if 'user' not in session:
        return redirect(url_for('iniciar_sesion'))

    usuario_actual = session['user']

    # Consultar Firebase para obtener los datos de los estudiantes
    alumnos_ref = db.collection('alumnos')
    datos_estudiantes = [doc.to_dict() for doc in alumnos_ref.get()]

    return render_template('visualizacion.html', usuario=usuario_actual, datos_estudiantes=datos_estudiantes)

if __name__ == "__main__":
    app.run(debug=True)
