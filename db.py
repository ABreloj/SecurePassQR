from flask import Flask, render_template, request, redirect, session, url_for  # Agrega la importación de url_for

import pymongo

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Asegúrate de usar una clave secreta segura en producción

# Función para obtener la conexión a la base de datos
def get_connection():
    return pymongo.MongoClient("mongodb://localhost:27017/")

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
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
            return render_template('iniciar_sesion.html', mensaje=mensaje)

        # Convertir ObjectId a cadena
        usuario_encontrado['_id'] = str(usuario_encontrado['_id'])

        session['user'] = usuario_encontrado
        return redirect('/visualizar')  # Redirigir a la página "visualizacion.html" después del inicio de sesión

    return render_template('Iniciar_Sesion.html')



@app.route('/visualizar')
def visualizar():
    # Verificar si el usuario ha iniciado sesión
    if 'user' not in session:
        return redirect(url_for('iniciar_sesion'))

    # Obtener el usuario de la sesión
    usuario_actual = session['user']

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


if __name__ == "__main__":
    app.run(debug=True)
