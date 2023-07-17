#!/bin/bash
SSl_authz=/etc/letsencrypt/live/esa.authz.smodata.net/fullchain.pem
if [ -e $SSl_authz ]; then
  echo "Hello";
  else
  certbot certonly --webroot --webroot-path /var/ --email esa.authz@smodata.net --no-eff-email --agree-tos --dry-run -d esa.authz.smodata.net;
fi

#set -o nounset
#set -o errexit

# May or may not have HOME set, and this drops stuff into ~/.local.
#export HOME="/root"
#export PATH="${PATH}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Install system dependencies
#apt update
#apt install python3 python3-venv libaugeas0 -y
## Set up a Python virtual environment
#python3 -m venv /opt/certbot/
#/opt/certbot/bin/pip install --upgrade pip
## Install Certbot
#/opt/certbot/bin/pip install certbot certbot-nginx
## Prepare the Certbot command
#ln -s /opt/certbot/bin/certbot /usr/bin/certbot
#
#certbot certonly --nginx --email esa.authz@smodata.net --no-eff-email --agree-tos -d esa.authz.smodata.net
## Set up config file.
#mkdir -p /etc/letsencrypt
#cat > /etc/letsencrypt/cli.ini <<EOF
## Uncomment to use the staging/testing server - avoids rate limiting.
#server = https://acme-staging.api.letsencrypt.org/directory
#
## Use a 4096 bit RSA key instead of 2048.
#rsa-key-size = 4096
#
## Set email and domains.
#email = esa.authz@smodata.net
#domains = esa.authz.smodata.net, www.esa.authz.smodata.net
#
## No prompts.
#non-interactive = True
## Suppress the Terms of Service agreement interaction.
#agree-tos = True
#
## Use the webroot authenticator.
##authenticator = webroot
##webroot-path = /var/www/html
#EOF

# Obtain cert.
#certbot-auto certonly

# Set up daily cron job.
#CRON_SCRIPT="/etc/cron.daily/certbot-renew"

#cat > "${CRON_SCRIPT}" <<EOF
##!/bin/bash
#echo "0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab > /dev/null
#
## If the cert updated, we need to update the services using it.
#if service --status-all | grep -Fq 'nginx'; then
#  service nginx reload
#fi
#EOF
#chmod a+x "${CRON_SCRIPT}"