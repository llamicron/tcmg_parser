get_log:
	curl https://s3.amazonaws.com/tcmg476/http_access_log > http_access_log

test:
	python parse.py

build:
	docker build --tag=parse .

run:
	docker run parse
