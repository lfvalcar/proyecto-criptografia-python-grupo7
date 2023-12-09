###################
#####LIBRERÍAS#####
###################
from flask import Flask, render_template, request, url_for, redirect
# FUNCIONES
import funciones.functions as f
import funciones.functions_samba as fsmb
import funciones.functions_flask as fflask
import funciones.functions_salva as fsalva

app = Flask(__name__)

# INICIO
@app.route("/", methods=['GET','POST'] )
def home():
    if request.method=='POST': # El usuario envía una solicitud con una accion a llevar a cabo
            accion=request.form['accion'] # Se procesa la acción que el usuario quiere llevar a cabo
            
            if accion=='fin': # Si esa acción es "fin", entonces se borran las credenciales (cerrar sesión)
                fflask.borrar_credencial() # Borrar la credencial y archivos de la sesión
            elif accion=='inicio': # Si esa acción es "inicio", entonces se guardan las nuevas credenciales (inciar sesión)
                # Nuevas credenciales envíadas por el nuevo usuario
                usuario=request.form['usuario']
                password=request.form['password']
                recurso_compartido=request.form['carpeta_compartida']
                fflask.escribir_credencial(usuario,password,recurso_compartido) # Se guardan para futuros inicios de sesión

    cookie=fflask.leer_credencial() # Comprobar si tenemos credenciales guardadas

    if cookie==False: # Si no tenemos credenciales...
        return render_template("login.html") # Pagina de inicio de sesión para el servidor remoto
    
    # Si tenemos credenciales las extraemos
    usuario,password,recurso_compartido=fflask.extraer_credencial() # Se obtienen las credenciales
    
    return render_template("home.html")

# ALGORITMO SIMÉTRICO
@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    # Variables que almacenarán el resultado del desencriptado y encriptado
    resultado_desencriptado=None
    resultado_encriptado=None
    
    if request.method == 'POST': # El usuario envía una solicitud de encriptación o desencriptación
        # Traer del html los datos introducidos por el usuario a variables
        archivo=request.files['archivo'] # Archivo a cifrar
        algoritmo=request.form['algoritmo'] # Algortimo con el que se va a encriptar o desencriptar
        modo=request.form['modo'] # Objetivo (encriptar o desencriptar)

        # Encriptado
        if modo=='encriptacion': # Se inicia la encriptacion
            almacenamiento=request.form['almacenamiento'] # Donde se almacena el resultado
            
            # Algoritmo
            if algoritmo=='AES': # Se produce la encriptación simétrica con AES
                print('hola')
            elif algoritmo=='DES': # Se produce la encriptación simétrica con DES
                ruta_archivo=fflask.subir_archivo(archivo) # Se sube el archivo a la aplicación para el proceso
                clave=fsalva.generador_claves() # Se genera la clave necesaria para el cifrado simétrico DES
                ruta_archivo_encriptado,ruta_archivo_clave,nombre_archivo_encriptado,nombre_archivo_clave,resultado_encriptado=fsalva.cifrado(ruta_archivo,clave) # Se cifra el archivo y devuelve: el archivo encriptado,archivo con la clave,sus respectivos nombres y el resultado del proceso

            # Almacenamiento
            if almacenamiento=='local': # Se almacena los resultados de la encriptación en local
                fflask.descargar_archivos(ruta_archivo_encriptado,ruta_archivo_clave)
            elif almacenamiento=='compartida': # Se almacena los resultados de la encriptación en remoto
                cookie=fflask.leer_credencial() # Comprobar si tenemos credenciales guardadas
                
                if cookie==False: # Si no hay credencial almacenada avisa al usuario de que hace falta inciar sesión
                    return render_template("csimetrico.html",cookie=False)
                
                usuario,password,recurso_compartido=fflask.extraer_credencial() # Si hay credenciales se extraen
                
                conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                fsmb.subir_archivo_smb(ruta_archivo_encriptado,nombre_archivo_encriptado,recurso_compartido,conexion) # Subida del archivo encriptado
                
                conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                fsmb.subir_archivo_smb(ruta_archivo_clave,nombre_archivo_clave,recurso_compartido,conexion) # Subida del archivo clave
            
        # Desencriptado
        if modo=='desencriptacion': # Se inicia la desencriptación
            clave=request.files['clave'] # Archivo con la clave simétrica

            # Algoritmo
            if algoritmo=='AES': # Se produce la desencriptación simétrica con AES
                return render_template("csimetrico.html")
            elif algoritmo=='DES': # Se produce la desencriptación simétrica con DES
                ruta_archivo=fflask.subir_archivo(archivo) # Se sube el archivo a la aplicación para trabajar con él
                ruta_archivo_clave=fflask.subir_archivo(clave) # Se sube la clave a la aplicación
                ruta_archivo_desencriptado,resultado_desencriptado=fsalva.descifrado(ruta_archivo,ruta_archivo_clave) # Se produce el descifrado 
                return fflask.descargar_archivos(ruta_archivo_desencriptado) # Se envía el archivo al cliente

    # Dependiendo de los resultados se mostrarán mensajes de éxito o errores
    if resultado_encriptado==True:
        return render_template("csimetrico.html",resultado_encriptado=True) # Éxito de la encriptación
    elif resultado_desencriptado==True:
        return render_template("csimetrico.html",resultado_desencriptado=True) # Éxito de la desencriptación
    else:
        return render_template("csimetrico.html") # Página por defecto

# ALGORITMO ASIMÉTRICO
@app.route("/casimetrico/", methods=['GET','POST'])
def casimetrico():
    # Variables que almacenarán el resultado del desencriptado y encriptado
    resultado_desencriptado=None
    resultado_encriptado=None
    resultado_importacion=None
    resultado_generacion=None
    
    if request.method == 'POST': # El usuario envía una solicitud de encriptación o desencriptación
        # Traer del html los datos introducidos por el usuario a variables
        modo=request.form['modo'] # Objetivo (encriptar o desencriptar)
        print(modo)
        if modo=='generacion':
            nombre_real=request.form['nombre']
            cookie=fflask.leer_credencial() # Comprobar si tenemos credenciales guardadas
                
            if cookie==False: # Si no hay credencial almacenada avisa al usuario de que hace falta inciar sesión
               return render_template("casimetrico.html",cookieIn=False)
                
            usuario,password,recurso_compartido=fflask.extraer_credencial() # Si hay credenciales se extraen
            clave_privada,clave_publica,nombre_archivo_publica=fsalva.generar_claves_rsa(nombre_real)
            print(clave_publica,nombre_archivo_publica)
            conexion=fsmb.conexion_smb(usuario,password)
            fsmb.subir_archivo_smb(clave_publica,nombre_archivo_publica,recurso_compartido,conexion)
        elif modo=='importacion':
                archivo=request.files['archivo'] # Archivo a cifrar
                nombre_real=request.form['nombre']
                correo_real=request.form['correo']
                keyid_real=request.form['fingerprint']

                cookie=fflask.leer_credencial() # Comprobar si tenemos credenciales guardadas
                
                if cookie==False: # Si no hay credencial almacenada avisa al usuario de que hace falta inciar sesión
                    return render_template("casimetrico.html",cookieIn=False)
                
                usuario,password,recurso_compartido=fflask.extraer_credencial() # Si hay credenciales se extraen

                ruta_archivo_local=fflask.subir_archivo(archivo)

                resultado_importacion=fflask.escribir_propiedades(archivo.filename,ruta_archivo_local,nombre_real,correo_real,keyid_real)

                conexion=fsmb.conexion_smb(usuario,password)
                fsmb.subir_archivo_smb(ruta_archivo_local,archivo.filename,recurso_compartido,conexion)

        # Encriptado
        if modo=='encriptacion': # Se inicia la encriptacion
            archivo=request.files['archivo'] # Archivo a cifrar
            almacenamiento=request.form['almacenamiento'] # Donde se almacena el resultado
            clave=request.form['clave']
            fsmb.bajar_archivo_smb(clave)
            archivo_original=fflask.subir_archivo(archivo)
            archivo_cifrado=fsalva.cifrar_rsa(archivo_original,archivo.filename,clave_publica)
            return fflask.descargar_archivos(archivo_cifrado)
            # Almacenamiento
            if almacenamiento=='local': # Se almacena los resultados de la encriptación en local
                print('pruebas')
            elif almacenamiento=='compartida': # Se almacena los resultados de la encriptación en remoto
                cookie=fflask.leer_credencial() # Comprobar si tenemos credenciales guardadas
                
                if cookie==False: # Si no hay credencial almacenada avisa al usuario de que hace falta inciar sesión
                    return render_template("casimetrico.html",cookieEnc=False)
                
                usuario,password,recurso_compartido=fflask.extraer_credencial() # Si hay credenciales se extraen
            
        # Desencriptado
        elif modo=='desencriptacion': # Se inicia la desencriptación
            archivo=request.files['archivo'] # Archivo a cifrar
            archivo_cifrado_rsa=fflask.subir_archivo(archivo)
            arhivo_descifrado_rsa=fsalva.descifrar_rsa(archivo_cifrado_rsa,clave_privada)
            return fflask.descargar_archivos(arhivo_descifrado_rsa)
    # Dependiendo de los resultados se mostrarán mensajes de éxito o errores
    if resultado_encriptado==True:
        return render_template("casimetrico.html",resultado_encriptado=True) # Éxito de la encriptación
    elif resultado_desencriptado==True:
        return render_template("casimetrico.html",resultado_desencriptado=True) # Éxito de la desencriptación
    elif resultado_importacion==True:
        return render_template("casimetrico.html",resultado_importacion=True)
    else:
        return render_template("casimetrico.html") # Página por defecto

# ALGORITMO HÍBRIDO
@app.route("/chibrido/")
def chibrido():
    return render_template("chibrido.html")

# LISTADO DE LOS ARCHIVOS COMPARTIDOS
@app.route("/listadoArchivos/", methods=['POST','GET'])
def listar_archivos():
    cookie=fflask.leer_credencial() # Se comprueba si hay credenciales almacenadas

    if cookie==False: # Si no hay credenciales
        return redirect(url_for('home')) # Pagina de inicio de sesión para el servidor remoto

    usuario,password,recurso_compartido=fflask.extraer_credencial() # Si hay credenciales se extraen
    conexion=fsmb.conexion_smb(usuario,password) # Se realiza la conexión
    fsmb.listar_archivos_smb(recurso_compartido,conexion) # Se lista los archivos

    if request.method=='POST': # El usuario elige descargar un archivo
        nombre_archivo=request.form['nombre_archivo'] # Se obtiene el nombre del archivo seleccionado
        ruta_archivo_remoto=request.form['ruta_archivo_remoto'] # Se obtiene la ruta remota del archivo seleccionado
        accion=request.form['accion']

        conexion=fsmb.conexion_smb(usuario,password) # Se realiza la conexión
        ruta_archivo_descargado=fsmb.bajar_archivo_smb(nombre_archivo,ruta_archivo_remoto,recurso_compartido,conexion) # Se baja el archivo a la aplición

        if accion=='Descargar':
            return fflask.descargar_archivos(ruta_archivo_descargado) # Se envía el archivo al cliente
        elif accion=='Utilizar':
            return render_template("casimetrico.html",nombre_archivo=nombre_archivo)

    return render_template("listado_archivos.html")

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