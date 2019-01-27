get_log:
	curl https://s3.amazonaws.com/tcmg476/http_access_log > http_access_log

test:
	pytest test_parse.py

run:
	python parse.py
