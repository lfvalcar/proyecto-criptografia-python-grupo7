#!/bin/bash

set -e

bash ${SCRIPTS}/start.sh
source ${SCRIPTS}/users.sh

mainSMB(){
   users 
   /usr/sbin/smbd --foreground --no-process-group &
   /usr/sbin/apache2ctl -D FOREGROUND # Ejecución del servicio
}

mainSMB