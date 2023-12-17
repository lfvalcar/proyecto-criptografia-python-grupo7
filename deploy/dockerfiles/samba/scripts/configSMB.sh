#!/bin/bash

set -e

configSMB(){
    /usr/sbin/smbd --foreground --no-process-group
}