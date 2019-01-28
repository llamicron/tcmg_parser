FROM python:3-onbuild
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN make get_log
CMD ["make", "run"]
