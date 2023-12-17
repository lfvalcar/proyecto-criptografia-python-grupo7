# LIBRERÍAS
from flask import Flask, render_template, request, url_for, redirect

# FUNCIONES
import funciones.functions_simon as fsimon
import funciones.functions_samba as fsmb
import funciones.functions_ficheros as fficheros
import funciones.functions_salva as fsalva

app = Flask(__name__)

# INICIO
@app.route("/", methods=['GET','POST'] )
def home():
    # Definición de variables
    usuario=None

    # Solicitud
    if request.method=='POST':
            accion=request.form['accion'] # Se procesa la acción de la solicitud
            
            # Acción
            if accion=='fin': # Si esa acción es "fin", entonces se borran las credenciales (cerrar sesión)
                fficheros.borrar_credencial() # Borrar la credencial y archivos de la sesión
            elif accion=='inicio': # Si esa acción es "inicio", entonces se guardan las nuevas credenciales (inciar sesión)
                # Nuevas credenciales envíadas por el nuevo usuario
                usuario=request.form['usuario']
                password=request.form['password']
                recurso_compartido=request.form['carpeta_compartida']
                
                # Comprobación de credenciales en el inicio de sesión
                conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                if conexion==False:
                    return render_template("login.html",credencial=False) # Página de login en caso de conexión fallida
                else:
                    conexion.close() # Cerrar la conexión una vez comprobado de que funciona
                    fficheros.escribir_credencial(usuario,password,recurso_compartido) # Se guardan las credenciales para futuros inicios de sesión
                # END Comprobación de credenciales en el inicio de sesión
            # END Acción
    # END Solicitud
                    
    # Comprobación de credenciales almacenadas
    cookie=fficheros.leer_credencial()

    if cookie==False: # Si no tenemos credenciales...
        return render_template("login.html") # Pagina de login
    else:
        # Si tenemos credenciales las extraemos
        usuario,password,recurso_compartido=fficheros.extraer_credencial() # Se obtienen las credenciales
    # END Comprobación de credenciales almacenadas

    # Mensajes interactivos de la página
    if usuario is not None: # Página home del usuario o por defecto
        return render_template("home.html",usuario=usuario) # Página de de bienvenida al usuario
    else:
        return render_template("home.html") # Página de inicio
    # END Mensajes interactivos de la página

# ALGORITMO SIMÉTRICO
@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    # Definición de variables
    archivo_encriptado=None

    # Solicitud
    if request.method == 'POST':
        # Se procesan los datos de la solicitud
        archivo=request.files['archivo'] # Archivo a encriptar o encriptado
        algoritmo=request.form['algoritmo'] # Algortimo a utilizar
        modo=request.form['modo'] # Operación a realizar

        # Encriptado
        if modo=='encriptacion':
            almacenamiento=request.form['almacenamiento'] # Donde se almacena el resultado
            
            # Algoritmo
            if algoritmo=='AES':
                # Cifrado AES
                archivo_original=fficheros.subir_archivo(archivo) # Se sube el archivo a la aplicación para el proceso
                iv_aes=fsimon.generate_random_iv() # Se genera un iv aleatorio
                clave_aes=fsalva.generador_clave(16) # Se genera una clave aleatoria para el cifrado AES
                archivo_encriptado,archivo_clave_aes,archivo_iv_aes,nombre_archivo_iv_aes,nombre_archivo_encriptado,nombre_archivo_clave_aes=fsimon.cifrado_aes(archivo_original,clave_aes,iv_aes) # Cifrado AES
                # END Cifrado AES
            elif algoritmo=='DES':
                # Cifrado DES
                archivo_original=fficheros.subir_archivo(archivo) # Se sube el archivo a la aplicación para el proceso
                clave_des=fsalva.generador_clave(8) # Se genera la clave necesaria para el cifrado simétrico DES
                archivo_encriptado,archivo_clave_des,nombre_archivo_encriptado,nombre_archivo_clave_des=fsalva.cifrado_des(archivo_original,clave_des) # Se produce el cifrado DES
                # END Cifrado DES
            # END Algoritmo

            # Almacenamiento
            if almacenamiento=='local': # Se almacena los resultados de la encriptación en local
                # Local
                if algoritmo=='AES':
                    nombre_zip=nombre_archivo_encriptado+'_encriptado_aes.zip'
                    zip=fficheros.comprimir_archivos_zip(nombre_zip,archivo_encriptado,archivo_clave_aes,archivo_iv_aes) # Los resultados se guardan en un zip
                    return fficheros.descargar_archivos(zip)
                elif algoritmo=='DES':
                    nombre_zip=nombre_archivo_encriptado+'_encriptado_des.zip'
                    zip=fficheros.comprimir_archivos_zip(nombre_zip,archivo_encriptado,archivo_clave_des) # Los resultados se guardan en un zip
                    return fficheros.descargar_archivos(zip)
                # END Local
            elif almacenamiento=='compartida': # Se almacena los resultados de la encriptación en remoto
                # Compartida
                # Comprobación de credenciales para el servidor SMB
                cookie=fficheros.leer_credencial() # Comprobar si tenemos credenciales guardadas
                
                if cookie==False: # Si no hay credencial almacenada avisa al usuario de que hace falta inciar sesión
                    return render_template("csimetrico.html",credencial=False)
                else:
                    usuario,password,recurso_compartido=fficheros.extraer_credencial() # Si hay credenciales se extraen
                # END Comprobación de credenciales para el servidor SMB

                # Algoritmo
                if algoritmo=='AES':
                    conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                    fsmb.subir_archivo_smb(archivo_encriptado,nombre_archivo_encriptado,recurso_compartido,conexion) # Subida del archivo encriptado
                
                    conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                    fsmb.subir_archivo_smb(archivo_clave_aes,nombre_archivo_clave_aes,recurso_compartido,conexion) # Subida del archivo clave AES

                    conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                    fsmb.subir_archivo_smb(archivo_iv_aes,nombre_archivo_iv_aes,recurso_compartido,conexion) # Subida del archivo iv

                elif algoritmo=='DES':
                    conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                    fsmb.subir_archivo_smb(archivo_encriptado,nombre_archivo_encriptado,recurso_compartido,conexion) # Subida del archivo encriptado
                
                    conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                    fsmb.subir_archivo_smb(archivo_clave_des,nombre_archivo_clave_des,recurso_compartido,conexion) # Subida del archivo clave DES
                # END Algoritmo
                # END Compartida
            # END Almacenamiento
        # END Encriptado

        # Desencriptado
        if modo=='desencriptacion':
            clave=request.files['clave'] # Archivo con la clave simétrica

            # Algoritmo
            if algoritmo=='AES': # Se produce la desencriptación simétrica con AES
                iv=request.files['archivo_iv'] # Archivo con el iv
                # Descifrado AES
                archivo_encriptado=fficheros.subir_archivo(archivo) # Se sube el archivo a la aplicación para trabajar con él
                clave_aes=fficheros.subir_archivo(clave) # Se sube la clave a la aplicación
                archivo_iv=fficheros.subir_archivo(iv) # Se trae a la aplicación el archivo iv
                archivo_desencriptado=fsimon.descifrado_aes(archivo_encriptado,clave_aes,archivo_iv) # Descifrado AES

                return fficheros.descargar_archivos(archivo_desencriptado) # Se envía el archivo al usuario
                # END Descifrado AES
            elif algoritmo=='DES': # Se produce la desencriptación simétrica con DES
                # Descifrado DES
                archivo_encriptado=fficheros.subir_archivo(archivo) # Se sube el archivo a la aplicación para trabajar con él
                clave_des=fficheros.subir_archivo(clave) # Se sube la clave a la aplicación
                archivo_desencriptado=fsalva.descifrado_des(archivo_encriptado,clave_des) # Se produce el descifrado 
                
            # Saltan los errores si es que los hay antes de seguir con el proceso
                # Errores
                if archivo_desencriptado==False:
                    return render_template("csimetrico.html",clave_incorrecta=True) # En caso de error...
                # END Errores
                return fficheros.descargar_archivos(archivo_desencriptado) # Se envía el archivo al cliente
                # END Descifrado DES
            # END Algoritmo
        # END Desencriptado
    # END Solicitud
    # Mensajes interactivos de la página
    if archivo_encriptado is not None:
        return render_template("csimetrico.html",resultado_encriptado=True) # Éxito de la encriptación
    else:
        return render_template("csimetrico.html") # Página por defecto
    # END Mensajes interactivos de la página

# ALGORITMO ASIMÉTRICO
@app.route("/casimetrico/", methods=['GET','POST'])
def casimetrico():
    # Variables que almacenarán el resultado del desencriptado y encriptado
    resultado_importacion=None
    resultado_encriptado=None

    # Solicitud
    if request.method == 'POST':
        modo=request.form['modo'] # Objetivo (encriptar o desencriptar)
        # Generación de claves
        if modo=='generacion':
            nombre_real=request.form['nombre'] # Nombre para el par de claves generado

            # Comprobación de credenciales para el servidor SMB
            cookie=fficheros.leer_credencial() # Comprobar si tenemos credenciales guardadas
                
            if cookie==False: # Si no hay credencial almacenada avisa al usuario de que hace falta inciar sesión
               return render_template("casimetrico.html",cookieIn=False)
                
            usuario,password,recurso_compartido=fficheros.extraer_credencial() # Si hay credenciales se extraen
            # END Comprobación de credenciales para el servidor SMB

            clave_privada,clave_publica,nombre_archivo_publica=fsalva.generar_claves_rsa(nombre_real) # Generación del par claves
            
            # Se guarda la clave pública en el servidor SMB
            conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
            fsmb.subir_archivo_smb(clave_publica,nombre_archivo_publica,recurso_compartido,conexion) # Se sube la clave pública

            return fficheros.descargar_archivos(clave_privada) # Se envía la clave privada al usuario
        # END Generación de claves
        # Importación de claves públicas
        elif modo=='importacion':
                archivo=request.files['archivo'] # Archivo a cifrar

                # Comprobación de credenciales para el servidor SMB
                cookie=fficheros.leer_credencial() # Comprobar si tenemos credenciales guardadas
                
                if cookie==False: # Si no hay credencial almacenada avisa al usuario de que hace falta inciar sesión
                    return render_template("casimetrico.html",cookieIn=False)
                
                usuario,password,recurso_compartido=fficheros.extraer_credencial() # Si hay credenciales se extraen

                # END Comprobación de credenciales para el servidor SMB

                ruta_archivo_local=fficheros.subir_archivo(archivo) # Se sube la clave pública a la aplicación

                conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                fsmb.subir_archivo_smb(ruta_archivo_local,archivo.filename,recurso_compartido,conexion) # Se sube la clave pública al servidor SMB
                resultado_importacion=True
        # END Importación de claves públicas
                
        # Encriptado RSA
        if modo=='encriptacion':
            archivo=request.files['archivo'] # Archivo a cifrar
            clave=request.files['clave_publica'] # Clave pública
            almacenamiento=request.form['almacenamiento'] # Donde se almacena el resultado
            
            # Se suben los archivos a la aplicación para el proceso
            clave_publica=fficheros.subir_archivo(clave)
            archivo_original=fficheros.subir_archivo(archivo)

            archivo_cifrado,nombre_archivo_cifrado=fsalva.cifrar_rsa(archivo_original,archivo.filename,clave_publica) # Cifrado RSA
            resultado_encriptado=True
        # END Encriptado RSA
            # Almacenamiento
            if almacenamiento=='local':
                # Local
                return fficheros.descargar_archivos(archivo_cifrado) # Se envía el archivo al usuario
                # END Local
            elif almacenamiento=='compartida':
                # Compartida
                # Comprobación de credenciales para el servidor SMB
                cookie=fficheros.leer_credencial() # Comprobar si tenemos credenciales guardadas
            
                if cookie==False: # Si no hay credencial almacenada avisa al usuario de que hace falta inciar sesión
                    return render_template("casimetrico.html",cookieEnc=False)
            
                usuario,password,recurso_compartido=fficheros.extraer_credencial() # Si hay credenciales se extraen
                # END Comprobación de credenciales para el servidor SMB
                
                # Se suben los resultados al servidor SMB
                conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                fsmb.subir_archivo_smb(archivo_cifrado,nombre_archivo_cifrado,recurso_compartido,conexion) # Subida del archivo encriptado
                # END Compartida
            # END Almacenamiento
        # Desencriptado
        elif modo=='desencriptacion':
            # Desencriptado RSA
            archivo=request.files['archivo'] # Archivo encriptado
            clave=request.files['clave_privada'] # Clave privada
            # Se suben los archivos a la aplicación
            archivo_cifrado_rsa=fficheros.subir_archivo(archivo) 
            clave_privada=fficheros.subir_archivo(clave)

            arhivo_descifrado_rsa=fsalva.descifrar_rsa(archivo_cifrado_rsa,clave_privada) # Descifrado RSA
            return fficheros.descargar_archivos(arhivo_descifrado_rsa) # Se envía los resultados al usuario
            # END Desencriptado RSA
        # END Desencriptado
    # END Solicitud
    # Dependiendo de los resultados se mostrarán mensajes de éxito o errores
    if resultado_importacion==True:
        return render_template("casimetrico.html",resultado_importacion=True) # Página de éxito de la importación
    elif resultado_encriptado==True:
        return render_template("casimetrico.html",resultado_encriptado=True) # Página de éxito de la encriptación
    else:
        return render_template("casimetrico.html") # Página por defecto

# ALGORITMO HÍBRIDO
@app.route("/chibrido/",methods=['GET','POST'])
def chibrido():
    archivo_encriptado=None

    # Comprobación de credenciales para el servidor SMB
    cookie=fficheros.leer_credencial() # Se comprueba si hay credenciales almacenadas

    if cookie==False: # Si no hay credenciales
        return redirect(url_for('home')) # Pagina de inicio de sesión para el servidor remoto
    # END Comprobación de credenciales para el servidor SMB 

    # Solicitud
    if request.method == 'POST':
        archivo=request.files['archivo'] # Archivo a cifrar
        algoritmo=request.form['algoritmo'] # Algortimo con el que se va a encriptar o desencriptar
        modo=request.form['modo'] # Objetivo (encriptar o desencriptar)

        # Encriptado híbrido
        if modo=='encriptacion':
            clave=request.files['clave_publica'] # Clave pública
            clave_publica=fficheros.subir_archivo(clave) # Se sube el archivo a la aplicación

            # Algoritmo
            if algoritmo=='AES':
                archivo_original=fficheros.subir_archivo(archivo) # Se sube el archivo a la aplicación para el proceso
                iv_aes=fsimon.generate_random_iv() # Se genera el iv random
                clave_aes=fsalva.generador_clave(16) # Se genera la clave aleatoria
                
                # Encriptado del archivo con la clave AES
                archivo_encriptado,archivo_clave_aes,archivo_iv_aes,nombre_archivo_iv_aes,nombre_archivo_encriptado,nombre_archivo_clave_aes=fsimon.cifrado_aes(archivo_original,clave_aes,iv_aes)

                # Encriptado de la clave AES con la claves pública RSA
                archivo_clave_encriptado,nombre_archivo_clave_encriptado=fsalva.cifrar_rsa(archivo_clave_aes,nombre_archivo_clave_aes,clave_publica)

                # Se extraen las credenciales
                usuario,password,recurso_compartido=fficheros.extraer_credencial() # Si hay credenciales se extraen
                
                # Subida de los archivos al servidor SMB
                conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                fsmb.subir_archivo_smb(archivo_encriptado,nombre_archivo_encriptado,recurso_compartido,conexion) # Subida del archivo encriptado

                conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                fsmb.subir_archivo_smb(archivo_clave_encriptado,nombre_archivo_clave_encriptado,recurso_compartido,conexion) # Subida del archivo clave

                conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                fsmb.subir_archivo_smb(archivo_iv_aes,nombre_archivo_iv_aes,recurso_compartido,conexion) # Subida del archivo clave
                # END Subida de los archivos al servidor SMB

            elif algoritmo=='DES': # Se produce la encriptación simétrica con DES
                ruta_archivo=fficheros.subir_archivo(archivo) # Se sube el archivo a la aplicación para el proceso
                clave=fsalva.generador_clave(8) # Se genera la clave necesaria para el cifrado simétrico DES
                
                # Se cifra el archivo con la clave DES
                ruta_archivo_encriptado,ruta_archivo_clave,nombre_archivo_encriptado,nombre_archivo_clave=fsalva.cifrado_des(ruta_archivo,clave) # Se cifra el archivo y devuelve: el archivo encriptado,archivo con la clave,sus respectivos nombres y el resultado del proceso

                # Se cifra la clave DES con la clave pública RSA
                archivo_encriptado,nombre_archivo_cifrado=fsalva.cifrar_rsa(ruta_archivo_clave,nombre_archivo_clave,clave_publica)

                # Se extraen los archivos
                usuario,password,recurso_compartido=fficheros.extraer_credencial() # Si hay credenciales se extraen
                
                # Subida de los archivos al servidor SMB
                conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                fsmb.subir_archivo_smb(archivo_encriptado,nombre_archivo_cifrado,recurso_compartido,conexion) # Subida del archivo encriptado
                
                conexion=fsmb.conexion_smb(usuario,password) # Se produce la conexión
                fsmb.subir_archivo_smb(ruta_archivo_encriptado,nombre_archivo_encriptado,recurso_compartido,conexion) # Subida del archivo clave
                # END Subida de los archivos al servidor SMB
            # END Algoritmo
        # END Encriptado híbrido
        # Desencriptado híbrido
        elif modo=='desencriptacion': # Se inicia la desencriptación
            archivo=request.files['archivo'] # Archivo a descifrar
            clave_simetrica_encriptada=request.files['clave_simetrica_encriptada'] # Clave a cifrar
            clave_privada=request.files['clave_privada'] # Clave privada
            # Se suben los ficheros a la aplicación
            ruta_archivo=fficheros.subir_archivo(archivo)
            ruta_clave_privada=fficheros.subir_archivo(clave_privada)
            ruta_clave_simetrica_encriptada=fficheros.subir_archivo(clave_simetrica_encriptada)

            # Descifrado RSA de la clave simétrica 
            archivo_descifrado_rsa=fsalva.descifrar_rsa(ruta_clave_simetrica_encriptada,ruta_clave_privada)

            # Descifrado del archivo que contiene el mensaje
            if algoritmo=='DES':
                ruta_archivo_desencriptado=fsalva.descifrado_des(ruta_archivo,archivo_descifrado_rsa) # Se produce el descifrado 
            elif algoritmo=='AES':
                iv=request.files['archivo_iv'] # Archivo con el iv
                archivo_iv=fficheros.subir_archivo(iv) # Se trae a la aplicación el archivo iv
                ruta_archivo_desencriptado=fsimon.descifrado_aes(ruta_archivo,archivo_descifrado_rsa,archivo_iv) # Descifrado AES
            # Saltan los errores si es que los hay antes de seguir con el proceso
            # Errores
            if archivo_encriptado==False:
                return render_template("csimetrico.html",clave_incorrecta=True) # En caso de error...
            # END Errores

            #Se envía el archivo descifrado al usuario
            return fficheros.descargar_archivos(ruta_archivo_desencriptado)
        # END Desencriptado híbrido
    # END Solicitud
        
    # Control de resultados
    if archivo_encriptado is not None:
        return render_template("chibrido.html",resultado_encriptado=True) # Página de éxito de la encriptación
    else:
        return render_template("chibrido.html") # Página por defecto

# LISTADO DE LOS ARCHIVOS COMPARTIDOS
@app.route("/listadoArchivos/", methods=['POST','GET'])
def listar_archivos():
    # Comprobación de credenciales para el servidor SMB
    cookie=fficheros.leer_credencial() # Se comprueba si hay credenciales almacenadas

    if cookie==False: # Si no hay credenciales
        return redirect(url_for('home')) # Pagina de inicio de sesión para el servidor remoto
    # END Comprobación de credenciales para el servidor SMB

    usuario,password,recurso_compartido=fficheros.extraer_credencial() # Si hay credenciales se extraen
    conexion=fsmb.conexion_smb(usuario,password) # Se realiza la conexión
    fsmb.listar_archivos_smb(recurso_compartido,conexion) # Se lista los archivos

    # Solicitud
    if request.method=='POST':
        nombre_archivo=request.form['nombre_archivo'] # Se obtiene el nombre del archivo seleccionado
        ruta_archivo_remoto=request.form['ruta_archivo_remoto'] # Se obtiene la ruta remota del archivo seleccionado

        conexion=fsmb.conexion_smb(usuario,password) # Se realiza la conexión
        ruta_archivo_descargado=fsmb.bajar_archivo_smb(nombre_archivo,ruta_archivo_remoto,recurso_compartido,conexion) # Se baja el archivo a la aplición

        return fficheros.descargar_archivos(ruta_archivo_descargado) # Se envía el archivo al usuario
    # END Solicitud
    return render_template("listado_archivos.html") # Página por defecto

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