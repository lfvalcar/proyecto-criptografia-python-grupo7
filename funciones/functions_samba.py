###################
#####LIBRERÍAS#####
###################
from smb.SMBConnection import SMBConnection

############################
#####VARIABLES GLOBALES#####
############################
archivos_local='data/archivos' # Carpeta de la aplicacion para gestion de ficheros
archivos_encriptados_remoto='/archivos_encriptados' # Carpeta remota (samba) donde compartir archivos encriptados
claves_simetricas_remoto='/claves_simetricas' # Carpeta remota (samba) donde compartir claves simetricas
claves_publicas_remoto='/claves_publicas' # Carpeta remota (samba) donde compartir claves publicas
servidor='127.0.0.1' # IP del servidor

#################################################
#####FUNCIONES GESTIÓN DE FICHEROS EN SAMBA#####
################################################

# CONEXIÓN AL SERVIDOR
# Parametros de entrada:
    # Usuario,password --> usuario y contraseña con la que acceder al servidor
def conexion_smb(usuario,password):
    conexion = SMBConnection(usuario, password, usuario,servidor, use_ntlm_v2=True) # Crear la conexion con los parametros especificados
    assert conexion.connect(ip=servidor, port=2001) # Conectar a la conexion creada

    return conexion

# LISTAR ARCHIVO DEL SERVIDOR SAMBA
# Parametros de entrada:
    # recurso_compartido --> carpeta compartida del servidor donde listar los archivos
    # conexion --> conexion creada para utilizar para acceder al servidor
def listar_archivos_smb(recurso_compartido,conexion):
    try:
        carpetas=conexion.listPath(recurso_compartido,'/') # Listar directorios en la carpeta compartida
        
        # Inicializar las variables para el codigo html
        cabecera_html=''
        listado_html=''

        # Generar la cabecera html
        cabecera_html+='{% extends "layout.html" %}'
        cabecera_html+='{% block title %}'
        cabecera_html+='Listado Archivos'
        cabecera_html+='{% endblock %}'
        cabecera_html+='{% block content %}'
        cabecera_html+='<h1>Listado de archivos compartidos</h1>' # Generar el titulo principal

        # Generar una entrada html por cada directorio listado
        for carpeta in carpetas:
                if carpeta.filename.startswith('.'): # Omitir los directorios ocultos
                    continue
                
                listado_html+='<h2>'+carpeta.filename+'</h2>' # Generar una entrada html por cada directorio
                archivos=conexion.listPath(recurso_compartido,carpeta.filename) # Listar los archivos de cada directorio
                
                for archivo in archivos: 
                    if not archivo.isDirectory: # Omitimos los directorios
                        ruta_remoto='/'+carpeta.filename+'/'+archivo.filename # La ruta completa remota de cada archivo
                        # Generar por cada archivo un formulario html
                        listado_html+='<form method="post"'
                        listado_html+='<p>'+archivo.filename+'</p>' # Nombre del archivo
                        listado_html+='<input type="hidden" name="nombre_archivo" value="'+archivo.filename+'">' # Nombre del archivo
                        listado_html+='<input type="hidden" name="ruta_archivo_remoto" value="'+ruta_remoto+'">' # Ruta completa remota del archivo
                        listado_html+='<input type="submit" name="descargar" value="Descargar">' # Botón para efectuar el post y descargar el archivo
                        listado_html+='</form><br>'
    finally:
        conexion.close() # Cerrar la conexion
    
    final_listado_html='{% endblock %}' # Generar el cierre del codigo html
    with open('templates/listado_archivos.html','w') as html:
        # Insertar codigo html generado previamente
        html.write(cabecera_html)
        html.write(listado_html)
        html.write(final_listado_html)

# SUBIR ARCHIVO AL SERVIDOR SAMBA
# Parametros de entrada:
    # ruta_archivo_flask --> archivo almacenado en la aplicacion para subirlo a remoto
    # archivo --> archivo enviado por el usuario
    # recurso_compartido --> carpeta compartida del servidor donde listar los archivos
    # conexion --> conexion creada para utilizar para acceder al servidor
def subir_archivo_smb(ruta_archivo_local,nombre_archivo,recurso_compartido,conexion):
    try:
        with open(ruta_archivo_local, 'rb') as archivo:
            if nombre_archivo.endswith('.enc'): # Si el archivo subido es .enc se enviará a la carpeta de encriptados
                ruta_archivo_remoto=archivos_encriptados_remoto+'/'+nombre_archivo # Ruta del archivo completa remoto donde se ubicará
                conexion.storeFile(recurso_compartido,ruta_archivo_remoto,archivo) # Subir el contenido del archivo al servidor
            elif nombre_archivo.endswith('.des') or nombre_archivo.endswith('.aes'): # Si el archivo subido es .des o a.aes se enviará a la carpeta de claves simétricas 
                ruta_archivo_remoto=claves_simetricas_remoto+'/'+nombre_archivo 
                conexion.storeFile(recurso_compartido,ruta_archivo_remoto,archivo) 
            elif nombre_archivo.endswith('.pub'): # Si el archivo subido es .pub se enviará a la carpeta de claves públicas
                ruta_archivo_remoto=claves_publicas_remoto+'/'+nombre_archivo
                conexion.storeFile(recurso_compartido,ruta_archivo_remoto,archivo)
    finally:
        conexion.close() # Cerrar la conexion

# DESCARGAR ARCHIVO DEL SERVIDOR SAMBA
# Parametros de entrada:
    # nombre_archivo --> nombre del archivo a descargar
    # ruta_remoto --> ruta remota del archivo a descargar
    # recurso_compartido --> carpeta compartida del servidor donde listar los archivos
    # conexion --> conexion creada para utilizar para acceder al servidor
def bajar_archivo_smb(nombre_archivo,ruta_remoto,recurso_compartido,conexion):
    try:
        ruta_archivo_descargado=archivos_local+'/'+nombre_archivo # Ruta donde se guardará el archivo descargado del servidor
        with open(ruta_archivo_descargado, 'wb') as archivo:
            conexion.retrieveFile(recurso_compartido, ruta_remoto,archivo) # Descargar el archivo desde el servidor SMB

            return ruta_archivo_descargado
    finally:
        conexion.close() # Cerrar la conexion