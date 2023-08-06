FROM python:3.7.10-alpine3.12


WORKDIR /usr/src/app/django
COPY  requirements.txt /usr/src/app/django
RUN apk update  && \
	apk add --no-cache tzdata &&\
	apk add mc gcc make libc-dev musl-dev linux-headers pcre-dev mariadb-dev build-base vim &&\
    apk add python3-dev libffi-dev sshpass openssh  build-base openldap-dev 

RUN	pip install -r requirements.txt 

ENV TZ=America/Los_Angeles
