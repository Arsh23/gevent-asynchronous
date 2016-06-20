import sys
import re
import requests
from datetime import datetime

# Track the urls we've found
crawled = 0
startTime = datetime.now()

def crawler(u):
    '''A very simple web crawler'''
    global crawled

    # Crawl the page, print the status
    response = requests.get(u)
    print response.status_code, u

    # Extract some links to follow using a *really* bad regular expression
    for link in re.findall('<a href="(http.*?)"', response.content):

        # Limit to 10 pages
        if crawled < 10:
            crawled += 1
            crawler(link)

# Read the seed url from stdin
crawler(sys.argv[1])
print datetime.now() - startTime # Took 10.78 seconds and prints same url
