#!/bin/sh

envsubst < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/nginx.conf

sed -i "s|TOENVNAMESPACE|$NAMESPACE|g" /usr/share/nginx/html/main.js

nginx -g 'daemon off;'
