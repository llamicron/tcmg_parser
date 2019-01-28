get_log:
	curl https://s3.amazonaws.com/tcmg476/http_access_log > http_access_log

run:
	python parse.py

build_docker:
	docker build --tag=parse .

run_docker:
	docker run parse
