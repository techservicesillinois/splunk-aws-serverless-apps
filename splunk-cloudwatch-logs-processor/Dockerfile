FROM	node:6.10-alpine

WORKDIR	/usr/src

ENV	NPM_CONFIG_LOGLEVEL=error

RUN	apk update && apk add zip

COPY	index.js package.json /usr/src/

RUN	npm install --production && npm run build:zip;
