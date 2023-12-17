# LIBRERÍAS
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# GENERADOR IV ALEATORIO
def generate_random_iv(length=16):
    return os.urandom(length)

# CIFRADO AES
def cifrado_aes(file_path, key, iv):
    # Se añaden a las rutas de los archivos la extensiones dependiendo de cada uno
    ruta_archivo_encriptado = file_path + '.enc'
    ruta_archivo_clave = file_path + '.aes'
    ruta_archivo_iv = file_path + '.iv'

    # Obtener el nombre de los archivos quitando la parte de la izquierda de la ruta
    nombre_archivo_encriptado = os.path.basename(ruta_archivo_encriptado)
    nombre_archivo_clave = os.path.basename(ruta_archivo_clave)
    nombre_archivo_iv = os.path.basename(ruta_archivo_iv)

    # Leemos el contenido del archivo original almacenado en /data/archivos
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    # Preparar el cifrador AES con las propiedades especificadas
    cipher = Cipher(algorithms.AES(key.encode()), modes.CFB8(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Con el cifrador ciframos el mensaje obtenido anteriormente
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

     # Escribir el mensaje cifrado en un nuevo archivo al que la añadimos la extensión
    with open(ruta_archivo_encriptado, 'wb') as archivo:
        archivo.write(ciphertext)

    # Escribir la clave en un archivo separado
    with open(ruta_archivo_clave, 'w') as archivo:
        archivo.write(key)

    # Escribir el iv en un archivo separado
    with open(ruta_archivo_iv, 'wb') as archivo:
        archivo.write(iv)

    # Devolver los archivos procesados
    return ruta_archivo_encriptado,ruta_archivo_clave,ruta_archivo_iv,nombre_archivo_iv,nombre_archivo_encriptado,nombre_archivo_clave

# DESCIFRADO AES
def descifrado_aes(encrypted_file_path, key_file_path, iv_file_path):
    # Abrimos y leemos el contenido de los archivos (encriptado,clave y iv)
    with open(encrypted_file_path, 'rb') as file:
        ciphertext = file.read()

    with open(key_file_path, 'rb') as file:
        key = file.read()

    with open(iv_file_path, 'rb') as file:
        iv = file.read()

    # Control de errores
    # Probamos con try el código de dentro
    try:
        cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=default_backend())
    # Si de try sale error, se controla con las excepciones
    except ValueError: # Si es de tipo ValueError como una clave incorrecta y salta el return False
        return False # Error de la encriptación
    
    # Preparar el desencriptador
    decryptor = cipher.decryptor()
    # Desencriptamos el mensaje encriptado
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Crear la ruta para el archivo desencriptado
    ruta_archivo_desencriptado = encrypted_file_path[:-4] + '.desenc'

    # Guardar el mensaje descifrado en el archivo
    with open(ruta_archivo_desencriptado,'wb') as file:
        file.write(plaintext)

    # Devolver la ruta de ese archivo
    return ruta_archivo_desencriptado