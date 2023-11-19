# Librerias
# Samba
from smb.SMBConnection import SMBConnection

# Variables globales 
archivos_local='data/archivos' # Carpeta de la aplicacion para gestion de ficheros
archivos_encriptados_remoto='/archivos_encriptados' # Carpeta remota (samba) donde compartir archivos encriptados
claves_simetricas_remoto='/claves_simetricas' # Carpeta remota (samba) donde compartir claves simetricas
claves_publicas_remoto='/claves_publicas' # Carpeta remota (samba) donde compartir claves publicas
servidor='127.0.0.1' # IP del servidor

# Parametros de entrada:
# Usuario,password --> usuario y contraseña con la que acceder al servidor
def conexion_smb(usuario,password):
    conexion = SMBConnection(usuario, password, usuario,servidor, use_ntlm_v2=True) # Crear la conexion con los parametros especificados
    assert conexion.connect(ip=servidor, port=2001) # Conectar a la conexion creada

    return conexion # Devolver la conexion

# Listado de archivos Samba
# Parametros de entrada:
# recurso_compartido --> carpeta compartida del servidor donde listar los archivos
# carpeta --> carpeta dentro del recurso compartido que queremos listar, puede ser claves,archivos...
# conexion --> conexion creada para utilizar para acceder al servidor
def listar_archivos_smb(recurso_compartido,carpeta,conexion):
    try:
        listado=conexion.listPath(recurso_compartido,carpeta) # Listar archivos en la carpeta compartida
        # Inicializar las variables para el codigo html
        cabecera_html=''
        listado_html=''

        # Generar la cabecera html
        cabecera_html+='{% extends "layout.html" %}'
        cabeceral_html+='{% block title %}'
        cabecera_html+='Listado Archivos'
        cabecera_html+='{% endblock %}'
        cabecera_html+='{% block content %}'
        listado_html+='<h2>'+carpeta+'</h2>' # Generar el listado especificado html

        # Generar una entrada html por cada archivo listado
        for archivo in listado:
            if not archivo.isDirectory: # No listar directorios
                listado_html+='<p>'+archivo.filename+'</p>'
    finally:
        conexion.close() # Cerrar la conexion
    
    final_listado_html='{% endblock %}' # Generar el cierre del codigo html
    with open('templates/listado_archivos.html','a') as html:
        # Insertar codigo html generado previamente
        html.write(listado_html)
        html.write(final_listado_html)

# Subida de archivos a remoto
# Parametros de entrada:
# ruta_archivo_flask --> archivo almacenado en la aplicacion para subirlo a remoto
# archivo --> archivo enviado por el usuario
# recurso_compartido --> carpeta compartida del servidor donde listar los archivos
# conexion --> conexion creada para utilizar para acceder al servidor
def subir_archivo_smb(ruta_archivo_flask,archivo,recurso_compartido,conexion):
    try:
        nombre_archivo=archivo.filename # Obtenemos el nombre del archivo
        with open(ruta_archivo_flask, 'rb') as archivo:
            conexion.storeFile(recurso_compartido,nombre_archivo,archivo) # Subir el contenido del archivo al servidor
    finally:
        conexion.close() # Cerrar la conexion

# Subida de archivos a remoto
# Parametros de entrada:
# nombre_archivo --> nombre del archivo a subir
# recurso_compartido --> carpeta compartida del servidor donde listar los archivos
# conexion --> conexion creada para utilizar para acceder al servidor
def bajar_archivo_smb(nombre_archivo,recurso_compartido,conexion):
    try:
        with open(nombre_archivo, 'wb') as archivo:
            conexion.retrieveFile(recurso_compartido, '/',archivo) # Descargar el archivo desde el servidor SMB
    finally:
        conexion.close() # Cerrar la conexion