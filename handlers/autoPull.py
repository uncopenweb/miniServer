import tornado.web

class PullHandler(tornado.web.RequestHandler):
    def post(self):
        print self.request.body
    def get(self):
        print 'get'
        self.write('ok')
    
UrlMap = [(r"/autoPull/$", PullHandler)]
