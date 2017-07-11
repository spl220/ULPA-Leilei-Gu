#!/usr/bin/env bash

FQDN1=ulpa-dev.eresearch.unimelb.edu.au
CERT_LOC=/etc/ssl/localcerts
SERVICE=nginx

mkdir -p $CERT_LOC

openssl req -new -newkey rsa:4096 -sha256 -days 365 -nodes -x509 \
    -subj "/C=AU/ST=VIC/L=Parkville/O=UniMelb/OU=MeG/CN=$FQDN1" \
    -keyout $CERT_LOC/privkey.pem  -out $CERT_LOC/fullchain.pem

chmod 600 $CERT_LOC/*.pem

rm -f /etc/nginx/fullchain.pem
rm -f /etc/nginx/privkey.pem

ln -s $CERT_LOC/fullchain.pem /etc/nginx/
ln -s $CERT_LOC/privkey.pem /etc/nginx/

rm /etc/nginx/sites-enabled/ulpa.edu.au
ln -s /etc/nginx/sites-available/ulpa.edu.au.ssl /etc/nginx/sites-enabled/

service $SERVICE reload
