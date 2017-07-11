#!/usr/bin/env bash

certbot renew --webroot \
    --noninteractive \
    -w /var/www/html \
    --post-hook "service nginx reload"
