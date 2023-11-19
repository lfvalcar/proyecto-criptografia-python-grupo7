# Librerias
# Gestion de ficheros Flask
import os
from werkzeug.utils import secure_filename
from flask import send_file

# Variables globales 
archivos_local='data/archivos_local' # Carpeta de la aplicacion para gestion de ficheros

# Funciones de gestion de archivos Flask
# Subida de archivos
# Parametros de entrada:
# archivo --> archivo subido por el usuario
def subir_archivo(archivo):
    nombre_archivo=secure_filename(archivo.filename) # Comprobar con secure_filename de que el archivo no contenga caracteres no seguros
    archivo.save(os.path.join(archivos_local, nombre_archivo)) # Almacenar el archivo en Flask con la libreria OS
    ruta_archivo_subido=archivos_local+'/'+nombre_archivo # Obtener la ruta del archivo almacenado en string para otras funciones

    return ruta_archivo_subido # Devolver la ruta del archivo subido a la aplicacion

# Bajada de archivos Flask
# Parametros de enrada:
# ruta_archivo_flask --> ruta del archivo ubicado en la aplicacion a descargar por el usuario
def bajar_archivo(ruta_archivo_flask):
    return send_file(ruta_archivo_flask, as_attachment=True) # Usar send_file para enviar el archivo al usuario