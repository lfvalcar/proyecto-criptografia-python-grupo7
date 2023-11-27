###################
#####LIBRERÍAS#####
###################
from flask import Flask, render_template, request
# FUNCIONES
import funciones.functions as f
import funciones.functions_samba as fsmb
import funciones.functions_flask as fflask
import funciones.functions_salva as fsalva

app = Flask(__name__)

# INICIO
@app.route("/", methods=['GET','POST'] )
def home():
    if request.method=='POST': # El usuario termina la sesión
        fflask.borrar_credencial() # Borrar la credencial y archivos de la sesión
    return render_template("home.html")

# ALGORITMO SIMÉTRICO
@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    if request.method == 'POST': # El usuario envía una solicitud de encriptación o desencriptación
        # Traer del html los datos introducidos por el usuario a variables
        archivo=request.files['archivo'] # Archivo a cifrar
        algoritmo=request.form['algoritmo'] # Algortimo con el que se va a encriptar o desencriptar
        modo=request.form['modo'] # Objetivo (encriptar o desencriptar)

        # Encriptado
        if modo=='encriptar': # Se inicia la encriptacion
            almacenamiento=request.form['almacenamiento'] # Donde se almacena el resultado
            
            # Algoritmo
            if algoritmo=='AES': # Se produce la encriptación simétrica con AES
                return render_template("csimetrico.html")
            elif algoritmo=='DES': # Se produce la encriptación simétrica con DES
                ruta_archivo=fflask.subir_archivo(archivo)
                clave=fsalva.generador_claves()
                ruta_archivo_encriptado,ruta_archivo_clave=fsalva.cifrado(ruta_archivo,clave)
                return render_template("csimetrico.html")

            # Almacenamiento
            if almacenamiento=='local': # Se almacena los resultados de la encriptación en local
                return render_template("csimetrico.html")
            elif almacenamiento=='compartida': # Se almacena los resultados de la encriptación en remoto
                return render_template("csimetrico.html")
            
        # Desencriptado
        if modo=='desencriptar': # Se inicia la desencriptación
            clave=request.files['clave'] # Archivo con la clave simétrica

            # Algoritmo
            if algoritmo=='AES': # Se produce la desencriptación simétrica con AES
                return render_template("csimetrico.html")
            elif algoritmo=='DES': # Se produce la desencriptación simétrica con DES
                ruta_archivo=fflask.subir_archivo(archivo)
                ruta_archivo_clave=fflask.subir_archivo(archivo)
                fsalva.descifrado(ruta_archivo,ruta_archivo_clave)
                return render_template("csimetrico.html")

    return render_template("csimetrico.html")

# ALGORITMO ASIMÉTRICO
@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")

# ALGORITMO HÍBRIDO
@app.route("/chibrido/")
def chibrido():
    return render_template("chibrido.html")

# LISTADO DE LOS ARCHIVOS COMPARTIDOS
@app.route("/listadoArchivos/", methods=['POST','GET'])
def listar_archivos():
        cookie=fflask.leer_credencial() # Comprobar si hay credencial almacenada

        if cookie==True: # Si hay credencial almacenada
            usuario,password,recurso_compartido=fflask.extraer_credencial() # Se extrae y se utiliza
            conexion=fsmb.conexion_smb(usuario,password) # Se realiza la conexión
            fsmb.listar_archivos_smb(recurso_compartido,conexion) # Se lista los archivos
            
            if request.method=='POST': # El usuario elige descargar un archivo
                nombre_archivo=request.form['nombre_archivo'] # Se obtiene el nombre del archivo seleccionado
                ruta_archivo_remoto=request.form['ruta_archivo_remoto'] # Se obtiene la ruta remota del archivo seleccionado
                
                conexion=fsmb.conexion_smb(usuario,password) # Se realiza la conexión
                ruta_archivo_descargado=fsmb.bajar_archivo_smb(nombre_archivo,ruta_archivo_remoto,recurso_compartido,conexion) # Se baja el archivo a la aplición
                return fflask.bajar_archivo(ruta_archivo_descargado) # Se envía el archivo al cliente
            
            return render_template("listado_archivos.html")
        
        elif cookie==False:
            if request.method=='POST': # El usuario inicia sesión
                usuario=request.form['usuario'] # Usuario para iniciar sesión en el servidor
                password=request.form['password'] # Contraseña para iniciar sesión en el servidor
                recurso_compartido=request.form['carpeta_compartida'] # Carpeta compartida en el servidor
                
                fflask.escribir_credencial(usuario,password,recurso_compartido) # Una vez introducidas la credencial se guarda para futuros inicios
                
                return render_template("listado_archivos.html")
        return render_template("login.html") # Pagina de inicio de sesión para el servidor remoto

# SOBRE EL EQUIPO
@app.route("/about/")
def about():
    return render_template("about.html")

# DOCUMENTACIÓN DEL PROYECTO
@app.route("/doc/")
def doc():
    return render_template("doc.html")

# DATOS DE LA API
@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")