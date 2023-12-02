from Cryptodome.Cipher import DES
from random import sample

#GENERADOR DE CLAVES
# Declaramos la función con un argumento (longitud de la contraseña)
def generador_claves():
    longitud=8
 
    # Definimos los caracteres y simbolos
    
    abc_minusculas = "abcdefghijklmnopqrstuvwxyz"
    
    # upper() transforma las letras de una cadena en mayusculas
    abc_mayusculas = abc_minusculas.upper() 
    
    numeros = "0123456789"
    simbolos = "{}[]()*;/,_-"
    
    # Definimos la secuencia
    secuencia = abc_minusculas + abc_mayusculas + numeros + simbolos
    
    # Llamamos la función sample() utilizando la secuencia, y la longitud
    password_union = sample(secuencia, longitud)
    
    # Con join insertamos los elementos de una lista en una cadena
    password_result = "".join(password_union)
    
    # Retornamos la variables "password_result"
    return password_result

def cifrado(ruta_archivo, key):
    # Definir rutas para el archivo encriptado y la clave
    ruta_archivo_encriptado = ruta_archivo + '.enc'
    ruta_archivo_clave = ruta_archivo + '.des'
    nombre_archivo_encriptado = ruta_archivo_encriptado[14:]
    nombre_archivo_clave = ruta_archivo_clave[14:]

    # Leer el contenido del archivo en modo binario
    with open(ruta_archivo, 'rb') as archivo:
        plaintext = archivo.read()

    # Codificar la clave a bytes
    keyenc = key.encode()

    # Crear un objeto de cifrado DES en modo OFB (Output Feedback)
    cipher = DES.new(keyenc, DES.MODE_OFB)

    # Cifrar el texto plano y agregar el vector de inicialización (IV)
    msg = cipher.iv + cipher.encrypt(plaintext)

    # Escribir el mensaje cifrado en un nuevo archivo
    with open(ruta_archivo_encriptado, 'wb') as archivo:
        archivo.write(msg)

    # Escribir la clave en un archivo separado
    with open(ruta_archivo_clave, 'w') as archivo:
        archivo.write(key)

    # Devolver las rutas de los archivos encriptados y la clave
    return ruta_archivo_encriptado,ruta_archivo_clave,nombre_archivo_encriptado,nombre_archivo_clave,True

def descifrado(ruta_archivo_encriptado, ruta_archivo_clave):
    # Crear la ruta para el archivo desencriptado
    ruta_archivo_desencriptado = ruta_archivo_encriptado[:-4] + '.desenc'
    print(ruta_archivo_desencriptado)

    # Leer el mensaje encriptado desde el archivo
    with open(ruta_archivo_encriptado, 'rb') as archivo:
        msg = archivo.read()

    # Leer la clave desde el archivo
    with open(ruta_archivo_clave, 'r') as archivo:
        key = archivo.read()

    # Codificar la clave a bytes
    keyenc = key.encode()

    # Obtener el vector de inicialización (IV) del mensaje cifrado
    iv = msg[:8]

    # Crear un objeto de cifrado DES en modo OFB (Output Feedback) con el IV
    cipher = DES.new(keyenc, DES.MODE_OFB, iv=iv)

    # Descifrar el texto cifrado (excluyendo el IV)
    decrypted_text = cipher.decrypt(msg[8:])

    # Escribir el texto descifrado en un nuevo archivo
    with open(ruta_archivo_desencriptado, 'wb') as archivo:
        archivo.write(decrypted_text)

    # Devolver la ruta del archivo descifrado
    return ruta_archivo_desencriptado,True