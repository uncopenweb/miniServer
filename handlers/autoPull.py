import tornado.web
from tornado.web import HTTPError
import os
import subprocess
import logging
import json

ROOT = '/var/tmp/playpen'
GIT = '/usr/bin/git'

class PullHandler(tornado.web.RequestHandler):
    def post(self, branch):
        # translate the json payload sent by github
        payload = json.loads(self.get_argument('payload'))
        # get the repository info
        repo = payload['repository']
        # construct the read-only url
        url = repo['url'].replace('https', 'git')+'.git'
        # get the name of the project
        name = repo['name']
        # get the organization 
        organization = repo.get('organization', '')
        
        if not os.path.exists(os.path.join(ROOT, repo['name'])):
            # we only clone if it is one of ours
            if (organization != 'uncopenweb' or 
                not url.startswith('git://github.com/uncopenweb/')):
                logging.warning('attempt to autoPull not uncopenweb project')
                raise HTTPError(400)
            r = subprocess.call([GIT, 'clone', url], cwd=ROOT)
            if r:
                logging.warning('clone failed')
            else:
                logging.info('cloned ' + url)
            if branch:
                r = subprocess.call([GIT, 'checkout', branch], cwd=os.path.join(ROOT, name))
                if r:
                    logging.warning('checkout failed')
                else:
                    logging.info('checked out ' + branch)
        else:
            d = os.path.join(ROOT, name)
            if (organization != 'uncopenweb' or 
                not url.startswith('git://github.com/uncopenweb/')):
                # we'll pull even if it isn't ours if we've already cloned
                info = subprocess.Popen([GIT, 'remote', '-v'], 
                                        stdout=subprocess.PIPE,
                                        cwd=d).communicate()[0]
                if url not in info:
                    logging.warning('no pull for ' + url)
            if not branch:
                branch = 'master'
            r = subprocess.call([GIT, 'pull', 'origin', branch], cwd=d)
            if r:
                logging.warning('pull failed')
            else:
                logging.info('pulled ' + url)
    
UrlMap = [(r"/autoPull/(.*)$", PullHandler)]
