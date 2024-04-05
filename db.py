from flask import Flask, render_template, request, redirect, session, url_for
import firebase_admin
import hashlib

from firebase_admin import credentials, firestore

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'



# Ruta para iniciar sesión con datos de prueba


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
