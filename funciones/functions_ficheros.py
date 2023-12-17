# LIBRERÍAS
import os
import glob
from werkzeug.utils import secure_filename
from flask import send_file
from shutil import copyfile
import zipfile

# VARIABLES GLOBALES
archivos_local='data/archivos' # Carpeta de la aplicacion para gestion de ficheros
archivo_credencial='data/credencial' # Archivo donde de se almacena la credencial junto al recurso compartido
archivo_propiedades='data/propiedades'
keyring="data/keyring"

###################################################
#####FUNCIONES DE GESTIÓN DE FICHEROS EN FLASK#####
###################################################

# SUBIR ARCHIVO A FLASK
# Parametros de entrada:
    # archivo --> archivo subido por el usuario
def subir_archivo(archivo):
    nombre_archivo=secure_filename(archivo.filename) # Comprobar con secure_filename de que el archivo no contenga caracteres no seguros
    
    # Dependiendo de la extensión se guarda en una ruta u otra
    if nombre_archivo.endswith('.pem') or nombre_archivo.endswith('.pub') or nombre_archivo.endswith('.des') or nombre_archivo.endswith('.aes'):
        # Se alamcena en el llavero
        archivo.save(os.path.join(keyring, nombre_archivo)) # Almacenar el archivo en Flask con la libreria OS
        ruta_archivo_subido=keyring+'/'+nombre_archivo # Obtener la ruta del archivo almacenado en string para otras funciones
    else:
        # Se alamcena en los archivos de la aplicación
        archivo.save(os.path.join(archivos_local, nombre_archivo)) # Almacenar el archivo en Flask con la libreria OS
        ruta_archivo_subido=archivos_local+'/'+nombre_archivo # Obtener la ruta del archivo almacenado en string para otras funciones

    return ruta_archivo_subido # Devolver la ruta del archivo subido a la aplicacion y su nombre

# Guardar el/los archivos en el directorio seleccionado
# Parametros de enrada:
    # nombre_zip --> nombre del archivo zip a descargar
    # *archivos --> lista de archivos a descargar
def descargar_archivos(nombre_zip,*archivos):
    if len(archivos)>1: # Si es una archivo se descarga con send_file y si no se procede a la descargar de varios archivos
        # Verificar que haya al menos un archivo para comprimir
        if not archivos:
            raise ValueError("La lista de rutas de archivos está vacía.")

        # Crear la ruta completa del archivo zip
        ruta_zip=archivos_local+'/'+nombre_zip

        # Crear el archivo zip y agregar los archivos
        with zipfile.ZipFile(ruta_zip, 'w') as zipf:
            for archivo in archivos:
                # Obtener el nombre del archivo sin la ruta completa
                nombre_archivo=os.path.basename(archivo)
                # Agregar el archivo al zip
                zipf.write(archivo, nombre_archivo)

        return ruta_zip
    
    return send_file(archivos[0],as_attachment=True) # Enviar el archivo


##################################
#####GESTIÓN DE LA CREDENCIAL#####
##################################

# COMPROBAR SI HAY CREDENCIAL GUARDADA
def leer_credencial():
    with open(archivo_credencial,'r') as credencial:
        comprobacion=credencial.readline() # Leer la primera linea del archivo credencial que indica si hay o no credencial almacenada
        if comprobacion.strip()=='True': # Asegurar de que no haya saltos de lineas al comprobar la primera linea 
            return True # Hay credencial almacenada
        else:
            return False # No hay credencial almacenada

# ALMACENAR CREDENCIAL
# Parametros de entrada:
    # usuario,password --> usuario y contraseña a almacenar
    # recurso compartido --> carpeta compartida del servidor al que se accede a almacenar
def escribir_credencial(usuario,password,recurso_compartido):
    with open(archivo_credencial,'w') as credencial:
        contenido=usuario+':'+password+':'+recurso_compartido # Almacenar la credencial de esta sesion separando por : 
        credencial.write('True\n') # Primera línea que indica si la credencial está activa o no
        credencial.write(contenido) # Se almacena la credencial

# ELIMINAR CREDENCIAL
def borrar_credencial():
    with open(archivo_credencial,'w') as credencial:
        credencial.write('False') # Escribir False para identificar que no hay credencial almacenada

    # No solo se borra la credencial si no también los archivos locales de la sesión
    # Listar todos los archivos a borrar mediante expresiones regulares
    archivos=glob.glob(archivos_local+'/*') 
    archivos_keyring=glob.glob(keyring+'/*')

    # Se borra cada archivo de cada listado
    for archivo in archivos: 
            os.remove(archivo)
        
    for archivo in archivos_keyring:
            os.remove(archivo)

# EXTRACCIÓN DE LA CREDENCIAL
def extraer_credencial():
    with open(archivo_credencial,'r') as credencial:
        registro=credencial.readlines()[1] # Leer la segunda linea donde esta la credencial almacenada
        usuario, password, recurso_compartido=registro.split(':') # Gracias a que separamos por : al almcenar podemos separarlo por : al extraer
        
        return usuario,password,recurso_compartido # Devolver la credencial
    
