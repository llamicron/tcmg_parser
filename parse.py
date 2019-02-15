from urllib.request import urlretrieve
import os
import time
import re

URL = 'https://s3.amazonaws.com/tcmg476/http_access_log'
LOCAL_FILE = 'http_access_log'
pattern = r'(.*?) - (.*) \[(.*?)\] \"(.*?) (.*?)\"? HTTP\/\d.\d" (.*) (.*)'

# Get the file if needed
if not os.path.isfile(LOCAL_FILE):
    print('Getting file...\nThis may take a minute...')
    urlretrieve(URL, LOCAL_FILE)

# Don't time the file retrieval
START_TIME = time.time()

lines = open(LOCAL_FILE, 'r').readlines()
errors = []
# field map
m = {
    'original': 0,
    'timestamp': 3,
    'method': 4,
    'file': 5,
    'status_code': 6,
    'size': 7
}

status_codes = {
    '2xx': 0,
    '3xx': 0,
    '4xx': 0,
    '5xx': 0
}

files = {}
dates = {}
for line in lines:
    req = re.match(pattern, line)
    if not req:
        errors.append(req)
        continue

    # 4xx or 3xx or something
    status_code = req.group(m['status_code'])[0] + 'xx'
    status_codes[status_code] += 1

    file = req.group(m['file'])
    try:
        files[file] += 1
    except KeyError:
        files[file] = 0

    date = req.group(m['timestamp'])[0:11]

    try:
        dates[date] += 1
    except KeyError:
        dates[date] = 0

# Print parse time
print(str(round(time.time() - START_TIME, 2)) + ' seconds to parse')

# Wrap it up to make it easy to retrieve
parsed_data = {
    'dates': dates,
    'files': files,
    'status_codes': status_codes,
    'errors': errors
}
