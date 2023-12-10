###################
#####LIBRERÍAS#####
###################
import os
import glob
from werkzeug.utils import secure_filename
from flask import send_file
import tkinter
from tkinter import filedialog
from shutil import copyfile

############################
#####VARIABLES GLOBALES#####
############################
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
    if nombre_archivo.endswith('.pem') or nombre_archivo.endswith('.key'):
        archivo.save(os.path.join(keyring, nombre_archivo)) # Almacenar el archivo en Flask con la libreria OS
        ruta_archivo_subido=keyring+'/'+nombre_archivo # Obtener la ruta del archivo almacenado en string para otras funciones
    else:
        archivo.save(os.path.join(archivos_local, nombre_archivo)) # Almacenar el archivo en Flask con la libreria OS
        ruta_archivo_subido=archivos_local+'/'+nombre_archivo # Obtener la ruta del archivo almacenado en string para otras funciones

    return ruta_archivo_subido # Devolver la ruta del archivo subido a la aplicacion y su nombre

# DESCARGAR ARCHIVO DE FLASK
# Seleccionar la ruta en el ordenador del usuario para almacenar el archivo
# Parámetros de entrada:
    # titulo --> título de la ventana emergente
def ventana_dialogo_directorio(titulo):
    ventana=tkinter.Tk() # Ventana emergente
    ventana.withdraw() # Dibujar ventana
    directorio_destino=filedialog.askdirectory(title=titulo) # Obtener la respuesta de la selección en la ventana
    
    return directorio_destino

# Guardar el/los archivos en el directorio seleccionado
# Parametros de enrada:
    # directorio_destino --> ruta del archivo ubicado en la aplicacion a descargar por el usuario
    # *archivo --> lista de archivos a descargar
def descargar_archivos(*archivos):
    if len(archivos)>1: # Si es una archivo se descarga con send_file y si no se procede a la descargar de varios archivos
        for archivo in archivos:
            nombre_archivo=os.path.basename(archivo) # Obtener el nombre del archivo
            titulo='¿Donde guardamos: '+nombre_archivo+'?' # Título de la ventana de selección
            directorio_destino=ventana_dialogo_directorio(titulo) # Lanzar ventana emergente
        
            if not os.path.exists(directorio_destino): # Crear el directorio si no existe
                os.makedirs(directorio_destino)
        
            ruta_destino=os.path.join(directorio_destino, nombre_archivo) # Construir la ruta de destino
            copyfile(archivo, ruta_destino) # Copiar el archivo al directorio de destino
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
    archivos=glob.glob(archivos_local+'/*') # Listar todos los archivos a borrar mediante expresiones regulares

    for archivo in archivos: # Se borra cada archivo listado
            os.remove(archivo)

# EXTRACCIÓN DE LA CREDENCIAL
def extraer_credencial():
    with open(archivo_credencial,'r') as credencial:
        registro=credencial.readlines()[1] # Leer la segunda linea donde esta la credencial almacenada
        usuario, password, recurso_compartido=registro.split(':') # Gracias a que separamos por : al almcenar podemos separarlo por : al extraer
        
        return usuario,password,recurso_compartido # Devolver la credencial
    
###############################################
#####PROPIEDADES DE LAS CLAVES ASIMÉTRICAS#####
###############################################
# ALMACENAR PROPIEDADES DE UNA CLAVE
def escribir_propiedades(nombre_archivo,ruta_archivo_clave,nombre,email,id):
    with open(archivo_propiedades,'a') as propiedades:
        contenido=nombre_archivo+':'+ruta_archivo_clave+':'+nombre+':'+email+':'+id
        propiedades.write(contenido)
        return True

# EXTRAER PROPIEDADES DE UNA CLAVE
def extraer_propiedades(keyid):
    with open(archivo_propiedades,'r') as propiedades:
        registros=propiedades.readlines
        for registro in registros:
            nombre_archivo, ruta_archivo_clave, nombre, email, id=registro.split(':')
            if keyid==id:
                continue
        
        return nombre_archivo, ruta_archivo_clave, nombre, email, id