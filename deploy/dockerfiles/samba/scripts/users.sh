#!/bin/bash

set -e

users(){
    groupadd grupo7
    useradd -m -s /usr/bin/false -G grupo7 ${USER1}
    useradd -m -s /usr/bin/false -G grupo7 ${USER2}
    useradd -m -s /usr/bin/false -G grupo7 ${USER3}
    echo -e "${USER1_PASSWORD}\n${USER1_PASSWORD}" | smbpasswd -a -s ${USER1}
    echo -e "${USER2_PASSWORD}\n${USER2_PASSWORD}" | smbpasswd -a -s ${USER2}
    echo -e "${USER3_PASSWORD}\n${USER3_PASSWORD}" | smbpasswd -a -s ${USER3}
}