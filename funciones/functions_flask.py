###################
#####LIBRERÍAS#####
###################
import os
import glob
from werkzeug.utils import secure_filename
from flask import send_file

############################
#####VARIABLES GLOBALES#####
############################
archivos_local='data/archivos' # Carpeta de la aplicacion para gestion de ficheros
archivo_credencial='data/credencial' # Archivo donde de se almacena la credencial junto al recurso compartido

###################################################
#####FUNCIONES DE GESTIÓN DE FICHEROS EN FLASK#####
###################################################

# SUBIR ARCHIVO A FLASK
# Parametros de entrada:
    # archivo --> archivo subido por el usuario
def subir_archivo(archivo):
    nombre_archivo=secure_filename(archivo.filename) # Comprobar con secure_filename de que el archivo no contenga caracteres no seguros
    archivo.save(os.path.join(archivos_local, nombre_archivo)) # Almacenar el archivo en Flask con la libreria OS
    ruta_archivo_subido=archivos_local+'/'+nombre_archivo # Obtener la ruta del archivo almacenado en string para otras funciones

    return ruta_archivo_subido # Devolver la ruta del archivo subido a la aplicacion y su nombre

# DESCARGAR ARCHIVO DE FLASK
# Parametros de enrada:
    # ruta_archivo_flask --> ruta del archivo ubicado en la aplicacion a descargar por el usuario
def bajar_archivo(ruta_archivo_local):
    return send_file(ruta_archivo_local, as_attachment=True) # Usar send_file para enviar el archivo al usuario

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
    archivos=glob.glob(archivos_local+'/*') # Listar todos los archivos a borrar mediante expresiones regulares

    for archivo in archivos: # Se borra cada archivo listado
            os.remove(archivo)

# EXTRACCIÓN DE LA CREDENCIAL
def extraer_credencial():
    with open(archivo_credencial,'r') as credencial:
        registro=credencial.readlines()[1] # Leer la segunda linea donde esta la credencial almacenada
        usuario, password, recurso_compartido=registro.split(':') # Gracias a que separamos por : al almcenar podemos separarlo por : al extraer
        
        return usuario,password,recurso_compartido # Devolver la credencial