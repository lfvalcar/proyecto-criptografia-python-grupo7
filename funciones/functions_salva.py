# Librerías
from Cryptodome.Cipher import DES
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from random import sample
import os

# Variables globales
keyring='data/keyring' # Carpeta donde se almacenan las claves
archivos_aplicacion="data/archivos" # Carpeta donde se almacenan los archivos de la aplicación

#GENERADOR CLAVES DES ALEATORIO
def generador_clave(length):
    # Longitudad para las claves DES
    longitud=length
 
    # Definir los caracteres y simbolos
    abc_minusculas = "abcdefghijklmnopqrstuvwxyz"
    # upper() transforma las letras de una cadena en mayusculas
    abc_mayusculas = abc_minusculas.upper() 
    numeros = "0123456789"
    simbolos = "{}[]()*;/,_-"
    
    # Definir la secuencia
    secuencia = abc_minusculas + abc_mayusculas + numeros + simbolos
    
    # Llamar la función sample() utilizando la secuencia, y la longitud
    password_union = sample(secuencia, longitud)
    
    # Con join insertamos los elementos de una lista en una cadena
    password_result = "".join(password_union)

    # Retornar la variables "password_result"
    return password_result

# CIFRADO DES
def cifrado_des(ruta_archivo, clave):
    # Definir rutas para el archivo encriptado y la clave
    ruta_archivo_encriptado = ruta_archivo + '.enc'
    ruta_archivo_clave = ruta_archivo + '.des'

    # Obtener el nombre de los archivos
    nombre_archivo_encriptado = os.path.basename(ruta_archivo_encriptado)
    nombre_archivo_clave = os.path.basename(ruta_archivo_clave)

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
    # Probar con try el código de dentro
    try:
        # Crear un objeto de cifrado DES en modo OFB (Output Feedback) con el IV
        descifrador = DES.new(clave_enc, DES.MODE_OFB, iv=iv)
    # Si de try sale error se controla
    except ValueError:  # Si es de tipo ValueError como una clave incorrecta y salta el return False
        return False # Error de la encriptación

    # Descifrar el texto cifrado (excluyendo el IV)
    mensaje_desencriptado = descifrador.decrypt(mensaje[8:])

    # Escribir el texto descifrado en un nuevo archivo
    with open(ruta_archivo_desencriptado, 'wb') as archivo:
        archivo.write(mensaje_desencriptado)

    # Devolver la ruta del archivo descifrado
    return ruta_archivo_desencriptado

# GENERADOR PAR CLAVES RSA
def generar_claves_rsa(nombre_real):
    key = RSA.generate(2048) # Se genera el par de claves con el tamaño
    # Del par de claves se obtiene cada una por separado
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    nombre_archivo_publica=nombre_real+".pub"

    # Guardar las claves en archivos
    clave_publica=keyring+"/"+nombre_archivo_publica
    clave_privada=keyring+"/"+nombre_real+".pem"

    # Se guarda la clave privada en un archivo
    with open(clave_privada, "wb") as private_file:
        private_file.write(private_key)

    # Se guarda la clave pública en un archivo
    with open(clave_publica, "wb") as public_file:
        public_file.write(public_key)

    # Se devuelven los resultados
    return clave_privada,clave_publica,nombre_archivo_publica

# CIFRADO RSA
def cifrar_rsa(archivo_original,nombre_archivo_original,ruta_clave_publica):
    
    # Leer la clave pública
    clave_publica = open(ruta_clave_publica, "rb").read()
    key = RSA.import_key(clave_publica) # Transformar el conteido leido en una clave
    
    # A partir de la clave se prepara el cifrador
    cipher = PKCS1_OAEP.new(key)
    
    # Se lee el contenido del archivo original
    with open(archivo_original, "rb") as file:
        data = file.read()
        
    # Se cifra el contenido leeído
    ciphertext = cipher.encrypt(data)

    # Se preparan las rutas de los archivos
    nombre_archivo_encriptado=nombre_archivo_original+'.enc'
    archivo_cifrado=archivos_aplicacion+"/"+nombre_archivo_encriptado
    ruta_archivo_encriptado = archivo_cifrado

    # Se guarda el mensaje cifrado en el archivo encriptado
    with open(archivo_cifrado, "wb") as file:
        file.write(ciphertext)
        return ruta_archivo_encriptado,nombre_archivo_encriptado

# DESCIFRADO RSA
def descifrar_rsa(archivo_cifrado,ruta_clave_privada):
    
    # Se lee el contenido de la clave privada
    clave_privada = open(ruta_clave_privada, "rb").read()

    ruta_archivo_desencriptado_rsa = archivo_cifrado[:-4] + '.desenc'

    # Se trandorma el contenido leido en un objeto clave
    key = RSA.import_key(clave_privada)
    # Se prepara el cifrador
    cipher = PKCS1_OAEP.new(key)
    
    # Se lee el contenido del archivo encriptado
    with open(archivo_cifrado, "rb") as file:
        ciphertext = file.read()
        # Se cifra con el cifrador
        decrypted_data = cipher.decrypt(ciphertext)
    
    # Guardar mensaje cifrado en el archivo desencriptado
    with open(ruta_archivo_desencriptado_rsa, "wb") as file:
        file.write(decrypted_data)

    # Devolver la ruta del archivo
    return ruta_archivo_desencriptado_rsa