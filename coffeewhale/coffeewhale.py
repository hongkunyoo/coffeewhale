import json
import urllib2
import os
import time
import StringIO
import traceback
import sys
import datetime
import pytz
import ssl
import inspect


glob_conf_path = None

def conf(path):
    global glob_conf_path
    glob_conf_path = path
    

def inner_wrapper(func, channel, *args, **kargs):
    
    start = time.time()
    try:
        val = func(*args, **kargs)
        if not isinstance(val, dict):
            val = {"return_value": val}
    except Exception as e:
        tb_output = StringIO.StringIO()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, file=tb_output)
        val = dict()
        val['exception'] = str(e)
        print tb_output.getvalue()
        print e
    # val['exception2'] = str(tb_output.getvalue())
    end = time.time()
    val["func_name"] = func.__name__
    val["func"] = func
    val["argv"] = sys.argv
    val["channel"] = channel
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
    func = kargs["func"]
    del kargs['func']
    conf_file = glob_conf_path
    if conf_file is None:
    #     f_path = os.path.abspath(inspect.getmodule(func).__file__)
    #     f_path = '/'.join(f_path.split('/')[:-1])
    #     conf_file = f_path + '/conf.json'
        
    # if os.path.isfile(conf_file):
    #     with open(conf_file) as conf_file_f:
    #         configure = json.load(conf_file_f)
    # else:
        conf_file = '%s/.coffeewhale.json' % os.environ['HOME']
    if os.path.isfile(conf_file):
        with open(conf_file) as conf_file_f:
            configure = json.load(conf_file_f)
    else:
        print('configure file is not provided!')
        sys.exit(0)
    
    
    if 'channel' not in kargs or kargs['channel'] == None:
        channel = configure['default_channel']
        if 'channel' in kargs:
            del kargs['channel']    
    else:
        channel = kargs['channel']
        del kargs['channel']
    
    kargs["system"] = os.uname()[1]
    kargs["user"] = os.getlogin()
    
    my_dict = ""
    for k in kargs:
        my_dict += (k + ": " + str(kargs[k]) + "\n")
    mytz = pytz.timezone('Asia/Seoul')
    payload = {"text": "----------[%s]----------\n%s" % (datetime.datetime.now(mytz).strftime('%m-%d %H:%M'), my_dict),
               "icon_url": configure['icon_url'], "username": configure['username']}
    url = "https://hooks.slack.com/services/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"
    
    url = configure['channel'][channel]
    # print url
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    context = ssl._create_unverified_context()
    response = urllib2.urlopen(req, json.dumps(payload), context=context)
    
    return kargs
    

@alarmable
def run(val=1):
    start = time.time()
    print 'start'
    i = 1
    for i in xrange(10000000):
        i * 102
    print 'end'
    [0, 1][int(val)]
    t = time.time() - start

    d = dict()
    d['my_time'] = t
    d['accuracy'] = "70.5%"
    d['my_val'] = val
    # notify(time2=t)
    return d


if __name__ == "__main__":
    print run(sys.argv[1])
