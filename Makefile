help:
	@cat Makefile

run:
	python parse.py

server:
	python server.py

build_docker:
	docker build --tag=llamicron/tcmg_project_3 .

