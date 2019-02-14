import re
import operator
import requests

URL = 'https://s3.amazonaws.com/tcmg476/http_access_log'
LOCAL_FILE = 'test_http_access_log'

# Lots of comments in this file, i normally don't write this many

def parse_request(request_string):
    """
    This method takes in a request string, example below, and returns a dictionary of the data in the string.
    Easier to work with an object like this.

    Example:

    This:
        local - - [24/Oct/1994:14:02:01 -0600] "GET index.html HTTP/1.0" 200 391

    Becomes this:
        {
            'area': 'local',
            'timestamp': '24/Oct/1994:14:02:01 -0600',
            'method': 'GET',
            'file': 'index.html',
            'http_version': 'HTTP/1.0',
            'status_code': '200',
            'size': '391',
            # Keep the original for later on
            'original': 'local - - [24/Oct/1994:14:02:01 -0600] "GET index.html HTTP/1.0" 200 391'
        }
    """

    req = {}

    # keys are the attributes we want to store, and values are the regex patterns to find the data in the request string
    matches = {
        # attr: regex pattern
        'area':         '(remote|local)',
        'timestamp':    '\[(.+)\]',
        'method':       '\"(\w+)',
        'file':         '\"\w+ (.+?) ',
        'http_version': '\"\w+ .+? (\w+/(\d|\.)+)',
        'status_code':  '\" (\d+)',
        'size':         '\" \d+ (\d+)'
    }

    for key, pattern in matches.items():
        try:
            # Apply the pattern to the string and set the req[key]
            req[key] = re.search(pattern, request_string).group(1)
        except AttributeError as err:
            # If there isn't a match, set req[key] = ''
            req[key] = ''

    req['original'] = request_string
    return req

def get_log_file(url, local_file):
    print('Getting log file...')
    text = requests.get(url).text
    with open(local_file, 'w') as fi:
        fi.write(text)

# If the file isn't there (if there are less than 1000 lines)
if sum(1 for line in open(LOCAL_FILE)) == 0:
    # Get the full log file
    get_log_file(URL, LOCAL_FILE)

# Get a list of the lines in the file, one request per line
req_strings = open(LOCAL_FILE, 'r').readlines()
reqs = []
for req_string in req_strings:
    # For each line in the file, create a new request object and add it to the reqs list
    reqs.append(parse_request(req_string))



# We now have a list of request objects with keys and values instead of strings. We can start counting things to report stats.

print('-- Request counts --')
# The first one is easy
# Total number of requests; print the length of the requests list
print(str(len(reqs)) + ' total requests')


print('\n-- Requests by Date --')
# Lets get a list of the timestamps, cutting out any that are == '' (errors in the logfile)
dates = [d['timestamp'][0:11] for d in reqs if d['timestamp'] != '']

# Split the dates from '24/Oct/1994' to ['24', 'Oct', '1994'] for all the items
dates = [d.split('/') for d in dates]

# This creates a new dictionary with month names as keys, and the day numbers in a list as the value, ex.
# {
#     'Oct': [24, 24, 24, 25, 25, 26, 26, 27, 27, 27],
#     'Nov': [1, 2, 3, 3, 3, 4]
# }
# We retain duplicates so we can count them, that's how many requests were made each day
monthly = {}
for date in dates:
    if date[1] not in monthly.keys():
        monthly[date[1]] = []
    monthly[date[1]].append(date[0])

# For each month
for month, days in monthly.items():
    # Monthly
    # Just count the number of items in the `days` list
    print('\n-- ' + month + ' --')
    print(str(len(days)) + ' total requests')

    # Daily
    # For each day, print the amount of times that day occurs in the `days` list
    for day in set(days):
        print(str(days.count(day)) + ' requests on ' + month + ' ' + str(day))

    # Weekly
    # TODO: Do this


print('\n-- Request Status Codes -- ')


# Get a list of all the status codes, again retaining duplicates
status_codes = [c['status_code'] for c in reqs if c['status_code'] != '']


# Get a new list of status codes beginning in '4' (failed)
failed = [f for f in status_codes if f[0] == '4']
# Find the percentage failed, failed ÷ total
percentage_failed = round(len(failed) / len(status_codes), 3)
# Print the percentage in a nice way
print("% of failed requests (4xx status code): " + str(percentage_failed * 100) + "%")

# Same as above but with requests starting in '3'
redirected = [r for r in status_codes if r[0] == '3']
percentage_redirected = round(len(redirected) / len(status_codes), 3)
print("% of redirected requests (3xx status code): " + str(percentage_redirected * 100) + "%")


print('\n-- Files --')

# Get a list of requested files with duplicates
files = [f['file'] for f in reqs]

# Count how many times each file was requested with a dictionary
file_counts = {}
for fi in files:
    if fi not in file_counts.keys():
        file_counts[fi] = 0
    file_counts[fi] += 1


# Get the key with the highest value
most_requested_file = max(file_counts.items(), key=operator.itemgetter(1))[0]
print('most requested file is: ' + most_requested_file)

# Least requested files
# There are a lot with only 1 request, just print the amount instead of a name
least_requested_files = [f[0] for f in file_counts.items() if f[1] == 1]
print('There are ' + str(len(least_requested_files)) + ' files that were requested 1 time')

months = list(monthly.keys())

requests = []
for month in months:
    requests = [r['original'] for r in reqs if r['timestamp'][3:6] == month]

    # I know it says to write the logs to the same directory as the code but that makes my heart hurt
    with open('logs/' + month.lower() + '_request_log', 'w') as fi:
        for req in requests:
            fi.write(req)

print('\nMonthly log files created in logs/')

print('\nDone\n')
