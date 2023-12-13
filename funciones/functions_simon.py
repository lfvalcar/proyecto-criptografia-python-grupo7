import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_random_iv(length=16):
    return os.urandom(length)

def cifrado_aes(file_path, key, iv):
    ruta_archivo_encriptado = file_path + '.enc'
    ruta_archivo_clave = file_path + '.aes'
    ruta_archivo_iv = file_path + '.iv'

    # Obtener el nombre de los archivos
    nombre_archivo_encriptado = ruta_archivo_encriptado[14:]
    nombre_archivo_clave = ruta_archivo_clave[14:]
    nombre_archivo_iv = ruta_archivo_iv[14:]

    with open(file_path, 'rb') as file:
        plaintext = file.read()

    cipher = Cipher(algorithms.AES(key.encode()), modes.CFB8(iv), backend=default_backend())

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

     # Escribir el mensaje cifrado en un nuevo archivo
    with open(ruta_archivo_encriptado, 'wb') as archivo:
        archivo.write(ciphertext)

    # Escribir la clave en un archivo separado
    with open(ruta_archivo_clave, 'w') as archivo:
        archivo.write(key)

    # Escribir el iv en un archivo separado
    with open(ruta_archivo_iv, 'wb') as archivo:
        archivo.write(iv)

    return ruta_archivo_encriptado,ruta_archivo_clave,ruta_archivo_iv,nombre_archivo_iv,nombre_archivo_encriptado,nombre_archivo_clave

def descifrado_aes(encrypted_file_path, key_file_path, iv_file_path):
    with open(encrypted_file_path, 'rb') as file:
        ciphertext = file.read()

    with open(key_file_path, 'rb') as file:
        key = file.read()

    with open(iv_file_path, 'rb') as file:
        iv = file.read()

    # Control de errores
    # Probamos con try
    try:
        cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=default_backend())
    # Si de try sale error se controla y si es de tipo ValueError como una clave incorrecta y salta el return False
    except ValueError:
        return False # Error de la encriptación
    
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Crear la ruta para el archivo desencriptado
    ruta_archivo_desencriptado = encrypted_file_path[:-4] + '.desenc'

    with open(ruta_archivo_desencriptado,'wb') as file:
        file.write(plaintext)

    return ruta_archivo_desencriptado