run:
	python parse.py

server:
	python server.py

build_docker:
	docker build --tag=parse .

run_docker:
	docker run parse
