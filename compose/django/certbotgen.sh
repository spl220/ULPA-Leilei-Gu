#!/usr/bin/env bash

FQDN1=ulpa.edu.au
FQDN2=www.ulpa.edu.au
CERT_EMAIL=san.lin@unimelb.edu.au
SERVICE=nginx


if (( $(ps -ef | grep -v grep | grep $SERVICE | wc -l) > 0 ))
then
    echo "$SERVICE is running..."
else
    service $SERVICE start
fi

certbot certonly --webroot -w /var/www/html \
    -d $FQDN1 \
    -d $FQDN2 \
#    --test-cert --no-verify-ssl --debug \
    --non-interactive --agree-tos --quiet --verbose --email $CERT_EMAIL

rm -f /etc/nginx/fullchain.pem
rm -f /etc/nginx/privkey.pem

ln -s /etc/letsencrypt/live/$FQDN1/fullchain.pem /etc/nginx/
ln -s /etc/letsencrypt/live/$FQDN1/privkey.pem /etc/nginx/

rm /etc/nginx/sites-enabled/ulpa.edu.au
ln -s /etc/nginx/sites-available/ulpa.edu.au.ssl /etc/nginx/sites-enabled/

ln -s /certbotrenew.sh /etc/cron.monthly/

service $SERVICE reload
