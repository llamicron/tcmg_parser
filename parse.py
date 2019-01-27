import re

def parse_request(request_string):
    """
    This method takes in a request string, example below, and returns a dictionary of the data in the string.
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
            'size': '391'
        }
    """

    # Empty request object
    req = {}

    # keys are the attributes we want to store, and values are the regex patterns to find the data in the request string
    matches = {
        # attr: regex pattern
        'area': '(remote|local)',
        'timestamp': '\[(.+)\]',
        'method': '\"(\w+)',
        'file': '\"\w+ (.+?) ',
        'http_version': '\"\w+ .+? (\w+/(\d|\.)+)',
        'status_code': '\" (\d+)',
        'size': '\" \d+ (\d+)'
    }

    # For each key and pattern
    for key, pattern in matches.items():
        try:
            # Apply the pattern to the string and set the req[key]
            req[key] = re.search(pattern, request_string).group(1)
        except AttributeError as err:
            # If there isn't a match, set req[key] = ''
            req[key] = ''

    return req

# Here's our file
fi = "test_http_access_log"
# Get a list of the lines in the file
req_strings = open(fi, 'r').readlines()
reqs = []
for req_string in req_strings:
    # For each line in the file, create a new request object and add it to the reqs list
    reqs.append(parse_request(req_string))


# We now have a list of request objects with keys and values instead of strings. We can start counting things to report stats.

# The first one is easy
# Total number of requests; print the length of the requests list
print(len(reqs))

# The next one is a bit more challenging
# Get a list of the dates of all the requests, with duplicates (that's important)
dates = [d['timestamp'][0:11] for d in reqs]
# Loop through all the dates (a version without duplicates)
for date in set(dates):
    # Print the number of occurances of each date in the dates list (there's one for each request, that's why we kept the duplicates)
    if date == '':
        print(str(dates.count(date)) + " requests with an invalid timestamp")
    else:
        print(str(dates.count(date)) + " requests on " + date)

# We can do months in the exact same way, but exclude the day portion of the date string when we do our list comprehension. notice the '3' instead of '0'
dates = [d['timestamp'][3:11] for d in reqs]
for date in set(dates):
    if date == '':
        print(str(dates.count(date)) + " requests with an invalid timestamp")
    else:
        print(str(dates.count(date)) + " requests in " + date)

# Unfortunately we can't do weeks this way since that requires grouping day numbers. eg, 1-7, 8-14, etc.
# We'll have to find another way

# Let's start the same way, get a list of dates of all the requests with duplicates
dates = [d['timestamp'][0:11] for d in reqs]

# This gives is a list of touples. First value is day number, second is month
# [
#   ('24', 'Oct'),
#   ('25', 'Oct'),
#   ('26', 'Oct'),
#   ...
# ]
days = [d[0:2] for d in dates]
months = [d[3:6] for d in dates]
weekly = list(zip(days, months))

# Get rid of errors
weekly = [w for w in weekly if w[0] != '']
# Trim the list to only include every 7 days
weekly = [w for w in weekly if int(w[0]) % 7 == 0]

print(weekly)
