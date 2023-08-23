#!/bin/bash
cp conf/db/db_login.env.example /tmp
mv /tmp/db_login.env.example /tmp/db_login.env
ansible-vault decrypt --ask-vault-pass \
conf/certbot/privkey.pem \
conf/certbot/fullchain.pem