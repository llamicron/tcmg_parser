run:
	python parse.py

server:
	python server.py

build_docker:
	docker build --tag=parse .
