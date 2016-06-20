import gevent.monkey
gevent.monkey.patch_all()
# import gevent's monkey patch

import gevent
import sys
import re
import requests
from  datetime import datetime

crawled = 0
startTime = datetime.now()
greenlets = []

def crawler(u):
    global craawled

    response = requests.get(u)
    print response.status_code, u

    for link in re.findall('<a href="(http.*?)"', response.content):

        # if crawled < 10:
        #     crawled += 1
        #     crawler(link)

        # new code
        if len(greenlets) < 10:
            greenlets.append(gevent.spawn(crawler, link))
            # create new greenlet for each url

# crawler(sys.argv[1])
greenlets.append(gevent.spawn(crawler, sys.argv[1]))
# start greenlets
while len(greenlets) < 10:
    gevent.sleep(1)

# Wait for everything to complete
gevent.joinall(greenlets)
print datetime.now() - startTime # Took 7.073 seconds
