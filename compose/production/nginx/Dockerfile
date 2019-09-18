FROM nginx:1.17.1

# 替换为国内源
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
COPY ./compose/production/nginx/sources.list /etc/apt/
RUN apt-get update && apt-get install -y --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf

# Proxy configurations
COPY ./compose/production/nginx/includes/ /etc/nginx/includes/


