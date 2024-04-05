from flask import Flask, render_template, request, redirect, session, url_for
import firebase_admin
import hashlib

from firebase_admin import credentials, firestore

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Inicializar la aplicación de Firebase con la URL específica de tu base de datos
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://passqr-9141c-default-rtdb.firebaseio.com/'
})
db = firestore.client()

# Ruta para iniciar sesión con datos de prueba
@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['Password']

        # Hashear la contraseña ingresada por el usuario
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Consultar la colección de usuarios en Firebase
        usuarios_ref = db.collection('usuarios')
        query = usuarios_ref.where('Usuario', '==', usuario).where('PasswordHash', '==', hashed_password).limit(1)
        results = list(query.stream())

        # Impresiones para depuración
        print("Consulta realizada:", query)
        print("Resultados obtenidos:", results)

        if results:
            usuario_encontrado = results[0].to_dict()
            print("Usuario encontrado:", usuario_encontrado)

            session['user'] = usuario_encontrado
            return redirect('/visualizar')
        else:
            mensaje = 'Usuario no registrado o contraseña incorrecta'
            return render_template('iniciar_sesion.html', mensaje=mensaje)

    return render_template('iniciar_sesion.html')

# Ruta para visualizar datos de prueba
@app.route('/visualizar')
def visualizar():
    if 'user' not in session:
        return redirect(url_for('iniciar_sesion'))

    usuario_actual = session['user']

    # Datos de prueba para mostrar en la visualización
    datos_estudiantes = [
        {'Matricula': '12345', 'Nombre': 'Juan', 'Apellidos': 'Pérez', 'Carrera': 'Informática', 'Usuario': 'juanperez', 'Password': 'test123', 'Entrada': '08:00', 'Salida': '16:00'},
        {'Matricula': '54321', 'Nombre': 'María', 'Apellidos': 'González', 'Carrera': 'Ingeniería', 'Usuario': 'mariagonzalez', 'Password': 'password456', 'Entrada': '09:00', 'Salida': '17:00'},
        {'Matricula': '98765', 'Nombre': 'Pedro', 'Apellidos': 'Martínez', 'Carrera': 'Administración', 'Usuario': 'pedromartinez', 'Password': 'secure789', 'Entrada': '07:30', 'Salida': '15:30'}
    ]

    return render_template('visualizacion.html', usuario=usuario_actual, datos_estudiantes=datos_estudiantes)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
