# Variables globales
archivo_credencial='data/credencial' # Archivo donde de se almacena la credencial junto al recurso compartido

# Comprobar si la credencial esta almacenada o no
def leer_credencial():
    with open(archivo_credencial,'r') as credencial:
        comprobacion=credencial.readline() # Leer la primera linea del archivo credencial que indica si hay o no credencial almacenada
        if comprobacion.strip()=='True': # Asegurar de que no haya saltos de lineas al comprobar la primera linea 
            return True # Hay credencial almacenada
        else:
            return False # No hay credencial almacenada

# Almacenar credencial
# Parametros de entrada:
# usuario,password --> usuario y contraseña a almacenar
# recurso compartido --> carpeta compartida del servidor al que se accede a almacenar
def escribir_credencial(usuario,password,recurso_compartido):
    with open(archivo_credencial,'w') as credencial:
        contenido=usuario+':'+password+':'+recurso_compartido # Almacenar la credencial de esta sesion separando por : 
        credencial.write('True\n')
        credencial.write(contenido) 

# Eliminar la credencial
def borrar_credencial():
    with open(archivo_credencial,'w') as credencial:
        credencial.write('False') # Escribir False para identificar que no hay credencial almacenada

# Extraccion de la credencial para utilizarla
def extraer_credencial():
    with open(archivo_credencial,'r') as credencial:
        registro=credencial.readlines()[1] # Leer la segunda linea donde esta la credencial almacenada
        usuario, password, recurso_compartido=registro.split(':') # Gracias a que separamos por : al almcenar podemos separarlo por : al extraer
        
        return usuario,password,recurso_compartido # Devolver la credencial