# TCMG Project 3

This is the project about parsing a log file

# Environment
There are a few parts to the environment. Let's go through the files in this project:

* `Dockerfile`: specifies the docker container
* `http_access_log`: The http access log. It is plain text, about 50M
* `test_http_access_log`: A shorter version of the file above, only about 12k lines, used for testing
* `Makefile`: Specifies some `make` commands. Makes it easy for other people to run this code
* `.gitignore`: source control, pretty standard
* `readme.md`: This file
* `parse.py`: The code to parse the log file
* `test_parse.py`: Code to test tjhe code to parse the log file
* `requirements.txt`: This is required for docker to run properly. Normally we would specify the python packages we need the docker container to install, but we don't have any external pacakge. We can just leave it blank.

# How to run
Running this code requires docker. If you have docker installed, you probably also have make. Run this:
```
$ make run
```
If you don't have make, run this:
```
$ docker-compose up
```
