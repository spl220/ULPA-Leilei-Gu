FROM python:2.7.13

ENV PYTHONUNBUFFERED 1

# Set the timezone
ENV TZ=Australia/Melbourne
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
 && echo $TZ > /etc/timezone \
 && dpkg-reconfigure -f noninteractive tzdata

# Install Nginx, Certbot
COPY ./compose/django/backports.list /etc/apt/sources.list.d/

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    nginx \
 && apt-get install -t jessie-backports -y --no-install-recommends \
    certbot \
 && rm -rf /var/lib/apt/lists/*

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
 && ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80 443

COPY ./compose/django/ulpa.edu.au.ssl /etc/nginx/sites-available/ulpa.edu.au.ssl
COPY ./compose/django/ulpa.edu.au /etc/nginx/sites-available/ulpa.edu.au
RUN ln -s /etc/nginx/sites-available/ulpa.edu.au /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default

COPY ./compose/django/certbotgen.sh ./compose/django/certbotrenew.sh ./compose/django/certselfsigned.sh /
RUN chmod +x /certbotgen.sh && chmod +x /certbotrenew.sh && chmod +x /certselfsigned.sh

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/django/entrypoint.sh ./compose/django/gunicorn.sh /

RUN chmod +x /entrypoint.sh && chmod +x /gunicorn.sh

COPY . /app

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
