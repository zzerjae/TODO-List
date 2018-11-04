FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:jonathonf/python-3.6 && \
    apt-get update -y && \
    apt-get install -y build-essential python3.6 python3.6-dev python3-pip \
                       git libpq-dev postgresql postgresql-contrib

WORKDIR /code/
COPY . /code/

ENV DJANGO_SETTINGS_MODULE wintercoding.settings.prod

RUN rm /usr/bin/python3 && \
    ln -s /usr/bin/python3.6 /usr/bin/python3

RUN pip3 install pip --upgrade
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uwsgi", "--http", "0.0.0.0:80", \
              "--wsgi-file", "/code/wintercoding/wsgi.py", \
              "--master", \
              "--die-on-term", \
              "--single-interpreter", \
              "--harakiri", "30", \
              "--reload-on-rss", "512", \
              "--post-buffering-bufsize", "8192"]
