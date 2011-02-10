'''
A tornado-based server for miscellaneous services.

It runs whatever handlers it finds in the handlers sub folder.

:copyright: Gary Bishop 2010
:license: BSD
'''
import tornado.httpserver
import tornado.ioloop
import tornado.web
import os
import string
import random
import optparse
import logging

import myLogging

def generate_secret(seed):
    '''Generate the secret string for hmac'''
    random.seed(seed)
    return ''.join(random.choice(string.letters + string.digits + string.punctuation)
                   for i in range(100))

def run(port=8888, debug=False, seed=0):
    kwargs = {
        'cookie_secret': generate_secret(seed),
        'debug': debug
    }
    import handlers
    UrlMap = []
    for m in handlers.__all__:
        UrlMap.extend(getattr(handlers, m).UrlMap)

    application = tornado.web.Application(UrlMap, **kwargs)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
    

def run_from_args():
    '''
    Runs an instance of the torongo server with options pulled from the command
    line.
    '''
    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", dest="port", default=8888,
        help="server port number (default=8888)", type="int")
    parser.add_option("--logId", dest="logId", default='', type="str",
        help="identity in syslog (default log to stderr)")
    parser.add_option("--logLevel", dest="logLevel", default="warning", type="str",
        help="logging level (info|debug|warning|error)")
    parser.add_option("--debug", dest="debug", action="store_true", 
        default=False, help="enable Tornado debug mode w/ automatic loading (default=false)")
    parser.add_option("--seed", dest="seed", default=0, type="int",
        help="seed for the random number generator")
    (options, args) = parser.parse_args()
        
    # initialize logging
    if options.logId:
        id = '%s:%d' % (options.logId, os.getpid())
        myLogging.init(id, options.logLevel)
    logging.warning('startup')

    # run the server
    run(options.port, options.debug, options.seed)

if __name__ == "__main__":
    run_from_args()
