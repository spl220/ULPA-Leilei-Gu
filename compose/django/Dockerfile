FROM python:2.7.13

ENV PYTHONUNBUFFERED 1

# Set the timezone
ENV TZ=Australia/Melbourne
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
 && echo $TZ > /etc/timezone \
 && dpkg-reconfigure -f noninteractive tzdata

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/django/entrypoint.sh ./compose/django/gunicorn.sh /

RUN chmod +x /entrypoint.sh && chmod +x /gunicorn.sh

COPY . /app

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
