from flask import Flask, render_template, request, redirect, session, url_for
import firebase_admin
import hashlib

from firebase_admin import credentials, firestore

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Inicializar la aplicación de Firebase
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['Password']

        # Hashear la contraseña ingresada por el usuario
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Imprimir los valores para verificar
        print('Usuario ingresado:', usuario)
        print('Contraseña ingresada:', password)
        print('Contraseña hasheada:', hashed_password)

        usuarios_ref = db.collection('usuarios')
        query = usuarios_ref.where('Usuario', '==', usuario).where('Password', '==', hashed_password)
        results = query.get()

        print('Resultados de la consulta:', results)  # Agregar impresión de resultados

        if len(results) == 0:
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


@app.route('/about')  # Definir la ruta para la página "Acerca de nosotros"
def about():
    return render_template('about.html')  # Asegúrate de tener un archivo about.html en tu carpeta de plantillas


if __name__ == "__main__":
    app.run(debug=True)
