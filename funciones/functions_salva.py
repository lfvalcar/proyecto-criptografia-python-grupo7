# Librerías
from Cryptodome.Cipher import DES
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from random import sample

# Variables globales
keyring='data/keyring'
archivos_aplicacion="data/archivos"

#GENERADOR DE CLAVES DES
# Declaramos la función con un argumento (longitud de la contraseña)
def generador_clave(length):
    # Longitudad para las claves DES
    longitud=length
 
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

# CIFRADO DES
def cifrado_des(ruta_archivo, clave):
    # Definir rutas para el archivo encriptado y la clave
    ruta_archivo_encriptado = ruta_archivo + '.enc'
    ruta_archivo_clave = ruta_archivo + '.des'

    # Obtener el nombre de los archivos
    nombre_archivo_encriptado = ruta_archivo_encriptado[14:]
    nombre_archivo_clave = ruta_archivo_clave[14:]

    # Leer el contenido del archivo en modo binario
    with open(ruta_archivo, 'rb') as archivo:
        mensaje = archivo.read()

    # Codificar la clave a bytes
    clave_encode = clave.encode()

    # Crear un objeto de cifrado DES en modo OFB (Output Feedback)
    cifrador = DES.new(clave_encode, DES.MODE_OFB)

    # Cifrar el texto plano y agregar el vector de inicialización (IV)
    mensaje_encriptado = cifrador.iv + cifrador.encrypt(mensaje)

    # Escribir el mensaje cifrado en un nuevo archivo
    with open(ruta_archivo_encriptado, 'wb') as archivo:
        archivo.write(mensaje_encriptado)

    # Escribir la clave en un archivo separado
    with open(ruta_archivo_clave, 'w') as archivo:
        archivo.write(clave)

    # Devolver las rutas de los archivos encriptados y la clave
    return ruta_archivo_encriptado,ruta_archivo_clave,nombre_archivo_encriptado,nombre_archivo_clave

# DESCIFRADO DES
def descifrado_des(ruta_archivo_encriptado, ruta_archivo_clave):
    # Crear la ruta para el archivo desencriptado
    ruta_archivo_desencriptado = ruta_archivo_encriptado[:-4] + '.desenc'

    # Leer el mensaje encriptado desde el archivo
    with open(ruta_archivo_encriptado, 'rb') as archivo:
        mensaje = archivo.read()

    # Leer la clave desde el archivo
    with open(ruta_archivo_clave, 'r') as archivo:
        clave = archivo.read()

    # Codificar la clave a bytes
    clave_enc = clave.encode()

    # Obtener el vector de inicialización (IV) del mensaje cifrado
    iv = mensaje[:8]

    # Control de errores
    # Probamos
    try:
        # Crear un objeto de cifrado DES en modo OFB (Output Feedback) con el IV
        descifrador = DES.new(clave_enc, DES.MODE_OFB, iv=iv)
    # Si de try sale error se controla y si es de tipo ValueError como una clave incorrecta y salta el return False
    except ValueError:
        return False # Error de la encriptación

    # Descifrar el texto cifrado (excluyendo el IV)
    mensaje_desencriptado = descifrador.decrypt(mensaje[8:])

    # Escribir el texto descifrado en un nuevo archivo
    with open(ruta_archivo_desencriptado, 'wb') as archivo:
        archivo.write(mensaje_desencriptado)

    # Devolver la ruta del archivo descifrado
    return ruta_archivo_desencriptado

# GENERADOR DE CLAVES RSA
def generar_claves_rsa(nombre_real):
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    nombre_archivo_publica=nombre_real+".pub"
    # Guardar las claves en archivos
    clave_publica=keyring+"/"+nombre_archivo_publica
    clave_privada=keyring+"/"+nombre_real+".pem"

    with open(clave_privada, "wb") as private_file:
        private_file.write(private_key)

    with open(clave_publica, "wb") as public_file:
        public_file.write(public_key)
    return clave_privada,clave_publica,nombre_archivo_publica,True

# CIFRADO RSA
def cifrar_rsa(archivo_original,nombre_archivo_original,ruta_clave_publica):
    
    clave_publica = open(ruta_clave_publica, "rb").read()

    key = RSA.import_key(clave_publica)
    cipher = PKCS1_OAEP.new(key)
    
    with open(archivo_original, "rb") as file:
        data = file.read()
        ciphertext = cipher.encrypt(data)

    nombre_archivo_encriptado=nombre_archivo_original+'.enc'
    archivo_cifrado=archivos_aplicacion+"/"+nombre_archivo_encriptado
    ruta_archivo_encriptado = archivo_cifrado

    with open(archivo_cifrado, "wb") as file:
        file.write(ciphertext)
        return ruta_archivo_encriptado,nombre_archivo_encriptado

# DESCIFRADO RSA
def descifrar_rsa(archivo_cifrado,ruta_clave_privada):
    
    clave_privada = open(ruta_clave_privada, "rb").read()
    
    ruta_archivo_desencriptado_rsa = archivo_cifrado[:-4] + '.desenc'
    key = RSA.import_key(clave_privada)
    cipher = PKCS1_OAEP.new(key)
    
    with open(archivo_cifrado, "rb") as file:
        ciphertext = file.read()
        decrypted_data = cipher.decrypt(ciphertext)
    
    with open(ruta_archivo_desencriptado_rsa, "wb") as file:
        file.write(decrypted_data)
    return ruta_archivo_desencriptado_rsa