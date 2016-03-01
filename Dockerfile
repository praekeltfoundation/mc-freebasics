FROM python:2.7.10

RUN apt-get update && apt-get install -y --no-install-recommends \
	redis-server nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PROJECT_ROOT /deploy/
ENV DJANGO_SETTINGS_MODULE freebasics.settings
ENV MESOS_MARATHON_HOST http://servicehost:8080

WORKDIR /deploy/

COPY freebasics /deploy/freebasics
ADD manage.py /deploy/
ADD requirements.txt /deploy/
ADD requirements-dev.txt /deploy/
ADD setup.py /deploy/
ADD README.rst /deploy/
ADD VERSION /deploy/
ADD docker/docker-entrypoint.sh /deploy/
ADD docker/mc2.nginx.conf /etc/nginx/sites-enabled/
ADD docker/supervisord.conf /etc/
ADD docker/mc2.supervisor.conf /etc/supervisor/conf.d/

RUN pip install gunicorn supervisor "Django<1.9,>=1.8" && \
    pip install -e . && \
    rm -rf ~/.cache/pip

RUN rm /etc/nginx/sites-enabled/default

RUN mkdir -p /etc/supervisor/conf.d/
RUN mkdir -p /var/log/supervisor

RUN chmod +x /deploy/docker-entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/deploy/docker-entrypoint.sh"]
