from __future__ import print_function
import json
import traceback
import platform
import datetime
import pytz


try:
    from urllib.request import *
    from urllib.parse import *
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import *

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


glob_conf_path = None


def conf(path):
    global glob_conf_path
    glob_conf_path = path
    

def inner_wrapper(func, channel, *args, **kargs):
    
    start = time.time()
    val = {}
    try:
        func(*args, **kargs)
    except Exception as e:
        tb_output = StringIO()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, file=tb_output)
        val = dict()
        val['exception'] = str(e)
        print(tb_output.getvalue())
        print(e)
    # val['exception2'] = str(tb_output.getvalue())
    end = time.time()
    val["func_name"] = func.__name__
    val["url"] = channel
    elapsed = end - start
    if elapsed > 1:
        elapsed = int(elapsed)
    val["elapse"] = str(datetime.timedelta(seconds=elapsed))

    return notify(**val)


def alarmable(func):
    
    if callable(func):
        def wrapper(*args, **kargs):
            return inner_wrapper(func, None, *args, **kargs)
        return wrapper
    else:
        channel = func
        def alarmable_call(func):
            def wrapper(*args, **kargs):
                return inner_wrapper(func, channel, *args, **kargs)
            return wrapper
        return alarmable_call


def notify(**kargs):
    url = None
    if "COFFEE_WHALE_URL" in os.environ:
        url = os.environ['COFFEE_WHALE_URL']

    if 'url' in kargs:
        url = kargs['url']
        del kargs['url']

    if url is None:
        raise Exception('Provide url or COFFEE_WHALE_URL')

    kargs["argv"] = sys.argv
    kargs["system"] = platform.node()
    kargs["user"] = os.getlogin()
    
    my_dict = ""
    for k in kargs:
        my_dict += (k + ": " + str(kargs[k]) + "\n")
    mytz = pytz.timezone('Asia/Seoul')
    payload = {"text": "----------[%s]----------\n%s" % (datetime.datetime.now(mytz).strftime('%m-%d %H:%M'), my_dict),
               "icon_url": 'https://raw.githubusercontent.com/hongkunyoo/coffeewhale/master/coffee_whale_only_bg.png',
               "username": 'coffee-whale'}
    # url = "https://hooks.slack.com/services/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"

    # print url
    req = Request(url)
    req.add_header('Content-Type', 'application/json')
    context = ssl._create_unverified_context()

    f = json.dumps(payload)
    f = f.encode('utf-8')

    response = urlopen(req, data=f, context=context)
    
    return kargs
    

@alarmable
def run(val=1):
    start = time.time()
    # print 'start'
    i = 1
    for i in range(10000000):
        i * 102
    # print 'end'
    [0, 1][int(val)]
    t = time.time() - start

    d = dict()
    d['my_time'] = t
    d['accuracy'] = "70.5%"
    d['my_val'] = val
    # notify(time2=t)
    return d


if __name__ == "__main__":
    print(run())
