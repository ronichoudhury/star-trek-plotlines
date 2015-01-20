#!/bin/sh

hostname=$1
port=$2

if [ -z "${hostname}" -a -z "${port}" ]; then
    hostname="localhost"
    port="8000"
elif [ -z "${port}" ]; then
    port="${hostname}"
    hostname="localhost"
fi

if [ -z "${TANGELO}" ]; then
    TANGELO=tangelo
fi

me=`readlink -f ${0}`
here=`dirname ${me}`

cd ${here}/tangelo
${TANGELO} --hostname ${hostname} --port ${port} --root .
