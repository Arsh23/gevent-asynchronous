import gevent.monkey
gevent.monkey.patch_all()
# import gevent's monkey patch

import gevent.pool
import gevent.queue

import sys
import re
import requests
from  datetime import datetime

crawled = 0
startTime = datetime.now()
pool = gevent.pool.Pool(5)
queue = gevent.queue.Queue()

def crawler():
    global crawled

    while 1:
        try:
            u = queue.get(timeout=0)
            response = requests.get(u)
            print response.status_code, u

            for link in re.findall('<a href="(http.*?)"', response.content):

                if crawled < 10:
                    crawled += 1
                    queue.put(link)

        except gevent.queue.Empty:
            break

# Read the seed url from stdin
queue.put(sys.argv[1])
pool.spawn(crawler)

while not queue.empty() and not pool.free_count() == 5:
    gevent.sleep(0.1)
    for x in xrange(0, min(queue.qsize(), pool.free_count())):
        pool.spawn(crawler)

# Wait for everything to complete
pool.join()

print datetime.now() - startTime # Took 5.943 seconds, varying
