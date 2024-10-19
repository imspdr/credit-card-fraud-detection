# nginx
FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf.template /etc/nginx/nginx.conf.template
COPY ./build /usr/share/nginx/html

COPY ./docker_entrypoint.sh /etc/entrypoint.sh
RUN chmod +x /etc/entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/bin/sh", "-c", "/etc/entrypoint.sh"]
