FROM node:18-alpine

WORKDIR /usr/src/app/angular
RUN apk update  && \
	apk add mc  && \
	npm install -g @angular/cli && \
	apk add --no-cache tzdata	
ENV TZ=America/Los_Angeles
