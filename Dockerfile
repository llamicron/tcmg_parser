FROM python:3-onbuild
COPY . /usr/src/app
WORKDIR /usr/src/app
EXPOSE 5000
CMD ["make", "server"]
