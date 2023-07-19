#!/bin/bash
authz_cert_path=/etc/letsencrypt/live/esa.authz.smodata.net/fullchain.pem
if [ -e $authz_cert_path ]; then
  echo "Certificate is exist"
  while true; do sleep 3600; echo "The cerbot is not stopped"; done
else
  if certbot certonly -v \
    --webroot \
    --webroot-path /etc/letsencrypt \
    --agree-tos \
    --no-eff-email \
    --no-redirect \
    --email esa.authz@smodata.net \
    --agree-tos \
    -d esa.authz.smodata.net; then
    echo "Certificates is create"
  else
    echo "Something wrong"
  fi
fi
# Set up daily cron job.
CRON_SCRIPT="/etc/cron.daily/certbot-renew"
cat > "${CRON_SCRIPT}" <<EOF
#!/bin/bash
echo "0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab > /dev/null
EOF
chmod a+x "${CRON_SCRIPT}"