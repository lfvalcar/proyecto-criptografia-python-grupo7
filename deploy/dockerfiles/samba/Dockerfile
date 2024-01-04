# Dockerfile de la imagen samba-sad
# Partimos de la imagen base de debian
FROM lfvalcar/deb-base

# Argumentos
ARG IDRSA
ARG SSH_PORT
ARG SMB_PORT
ARG DOCKERFILE_SAMBA
ARG MEDIA
ARG HTTP_PORT

# Instalamos el paquete de samba
RUN apt update && apt upgrade -yq && apt install -yq --no-install-recommends \
    samba \
    apache2 \
    && apt autoremove -yq \
    && apt clean -yq

# Creación de carpetas necesarias
# Creación de la carpeta del proyecto
RUN mkdir -p /srv/anillos/GrupoSAD7
# Se situa en el directorio del proyecto
WORKDIR /srv/anillos/GrupoSAD7
# Creación de las carpetas necearias
RUN mkdir claves_simetricas claves_publicas archivos_encriptados archivos_ivs
# Permisos para la compartición de las carpetas
RUN chmod 777 /srv/anillos/GrupoSAD7 -R

# Copiado de archivos
# Copiar la RSA para el ssh sin contraseña
COPY ${IDRSA} /root
# Copiar scripts para la configuración del servicio SMB
COPY ${DOCKERFILE_SAMBA}/scripts/* /root/scripts/
# Permisos de ejecución para los scritps
RUN chmod u+x /root/scripts -R
# Copiar archivo de configuración smb
COPY ${DOCKERFILE_SAMBA}/smb.conf /etc/samba
# Copiar las imágenes al servidor 
COPY ${MEDIA} /var/www/html

# Exponer puerto SMB
EXPOSE ${SMB_PORT}
EXPOSE ${HTTP_PORT}

# Entrypoint 
ENTRYPOINT [ "/root/scripts/start_smbd.sh" ]