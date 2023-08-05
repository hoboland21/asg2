FROM node:20-alpine3.17

WORKDIR /usr/src/app/angular
RUN apk update  && \
	apk add mc  && \
	npm install -g @angular/cli && \
	apk add --no-cache tzdata	
ENV TZ=America/Los_Angeles
