FROM python:3-onbuild
COPY . /usr/src/app
WORKDIR /usr/src/app
CMD ["make", "server"]
