FROM nginx:1.17.1

RUN apt-get update && apt-get install -y --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY ./compose/production/nginx/conf.d/*.conf /etc/nginx/conf.d/
# Proxy configurations
COPY ./compose/production/nginx/includes/ /etc/nginx/includes/


