import re

LOCAL_FILE = 'test_http_access_log'

pattern = r'(.*?) - - \[(.*)] \"(.*?) (.*?\..*?) (HTTP\/\d\.\d)\" (\d*) (\d*)'

with open(LOCAL_FILE, 'r') as fi:

    lines = fi.readlines()


for line in lines:
    match = re.match(pattern, line)
    if match:
        print(match.group(2))
