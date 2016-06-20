import gevent.monkey
gevent.monkey.patch_all()
# import gevent's monkey patch

import gevent.pool
import sys
import re
import requests
from  datetime import datetime

crawled = 0
startTime = datetime.now()
pool = gevent.pool.Pool(5)

def crawler(u):
    global crawled

    response = requests.get(u)
    print response.status_code, u

    for link in re.findall('<a href="(http.*?)"', response.content):

        if crawled < 10 and not pool.full():
            crawled += 1
            pool.spawn(crawler, link)

# Read the seed url from stdin
pool.spawn(crawler, sys.argv[1])

# Wait for everything to complete
pool.join()

print datetime.now() - startTime # Took 6.943 seconds, varying
