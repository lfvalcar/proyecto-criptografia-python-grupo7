# Librerias
# Aplicacion
from flask import Flask, render_template, request
# Funciones de gestion ficheros
import funciones.functions as f
import funciones.functions_samba as fsmb
import funciones.functions_flask as fflask

app = Flask(__name__)

# Raíz del proyecto
@app.route("/", methods=['GET','POST'] )
def home():
    return render_template("home.html")

# Cifrado simétrico
@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    return render_template("csimetrico.html")

# Cifrado Asimétrico
@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")

# Cifrado Híbrido
@app.route("/chibrido/")
def chibrido():
    return render_template("chibrido.html")

# Listado de los archivos compartidos
@app.route("/listadoArchivos/", methods=['GET','POST'])
def listar_archivos():
        return render_template("login.html")

# Sobre el equipo
@app.route("/about/")
def about():
    return render_template("about.html")

# Documentación del proyecto
@app.route("/doc/")
def doc():
    return render_template("doc.html")

# Datos de la api
@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

if __name__ == '__main__':
    app.run(debug=True)
