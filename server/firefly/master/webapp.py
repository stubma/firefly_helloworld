#coding:utf8
'''
Created on 2013-8-7

@author: lan (www.9miao.com)
'''
import os
from twisted.web.resource import Resource, NoResource
from twisted.internet import reactor
from firefly.server.globalobject import GlobalObject

def ErrorBack(reason):
    pass

def getFileData(filename):
    with open(filename) as f:
        return f.read()

class StopHandle(Resource):
    '''stop service'''
    
    def render(self, request):
        for child in GlobalObject().root.childsmanager._childs.values():
            d = child.callbackChild('serverStop')
            d.addCallback(ErrorBack)
        reactor.callLater(0.5,reactor.stop)
        return "stop"

class ReloadHandle(Resource):
    '''reload module'''
    
    def render(self, request):
        for child in GlobalObject().root.childsmanager._childs.values():
            d = child.callbackChild('sreload')
            d.addCallback(ErrorBack)
        return "reload"

class AdminHandle(Resource):
    ''' admin resource '''

    def render(self, request):
        dir = os.path.dirname(__file__)
        dir = os.path.dirname(dir)
        dir = os.path.dirname(dir)
        file = dir + '/webroot/index.html'
        return getFileData(file)

class MasterDirectory(Resource):
    '''
    default root resource of master web service
    '''

    def __init__(self):
        Resource.__init__(self)
        GlobalObject().webroot.putChild('stop', StopHandle())
        GlobalObject().webroot.putChild('reload', ReloadHandle())
        GlobalObject().webroot.putChild('admin', AdminHandle())

    def getChild(self, path, request):
        # by default, index.html or empty path redirect to admin
        if path is None or path == '' or path == 'index.html':
            return GlobalObject().webroot.getChildWithDefault('admin', request)

        # for other, just 404
        return NoResource("No Such Resource")
