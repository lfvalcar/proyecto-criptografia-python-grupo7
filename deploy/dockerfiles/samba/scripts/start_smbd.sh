#!/bin/bash

set -e

bash ${SCRIPTS}/start.sh
source ${SCRIPTS}/users.sh
source ${SCRIPTS}/configSMB.sh

mainSMB(){
   users 
   configSMB
}

mainSMB
tail -f /dev/null 