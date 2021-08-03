#!/bin/bash

function configSSH
{
    echo 'root:111111' | chpasswd
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
    echo 'cd /usr/src >& /dev/null' >> /root/.bashrc
    service ssh start || true
}

configSSH

cd app

case $1 in
    --stag)
        python3 main.py --stag
        ;;
    --prod)
        python3 main.py --prod
        ;;
esac

