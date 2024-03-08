from flask import Flask, render_template, request

app = Flask(__name__)

# Tu código de conexión a MongoDB
import pymongo
cliente = pymongo.MongoClient("mongodb://localhost:27017/")
mi_base_de_datos = cliente["SecurePassQR"]
mi_coleccion = mi_base_de_datos["Alumnos"]

@app.route("/", methods=["GET", "POST"])
def inicio_sesion():
    if request.method == "POST":
        # Obtiene los datos del formulario
        usuario = request.form.get("usuario")
        contrasena = request.form.get("contrasena")

        # Verifica las credenciales en la base de datos
        usuario_encontrado = mi_coleccion.find_one({"Usuario": usuario, "Contraseña": contrasena})

        if usuario_encontrado:
            # Aquí podrías redirigir al usuario a una página de inicio de sesión exitosa
            return "Inicio de sesión exitoso"
        else:
            # Aquí podrías mostrar un mensaje de error al usuario
            return "Usuario o contraseña incorrectos"

    return render_template("tu_archivo_html.html")

if __name__ == "__main__":
    app.run(debug=True)
