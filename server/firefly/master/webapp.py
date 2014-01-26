#coding:utf8
'''
Created on 2013-8-7

@author: lan (www.9miao.com)
'''
from twisted.web.resource import Resource
from twisted.internet import reactor
from firefly.server.globalobject import GlobalObject

def ErrorBack(reason):
    pass

class StopHandle(Resource):
    '''stop service'''
    
    def render(self, request):
        for child in GlobalObject().root.childsmanager._childs.values():
            d = child.callbackChild('serverStop')
            d.addCallback(ErrorBack)
        reactor.callLater(0.5, reactor.stop)
        return "stop"

class ReloadHandle(Resource):
    '''reload module'''
    
    def render(self, request):
        for child in GlobalObject().root.childsmanager._childs.values():
            d = child.callbackChild('sreload')
            d.addCallback(ErrorBack)
        return "reload"

class DefaultMasterDirectory(Resource):
    '''
    default root resource of master web service
    '''

    def __init__(self):
        Resource.__init__(self)

        # register static handle
        GlobalObject().webroot.putChild('stop', StopHandle())
        GlobalObject().webroot.putChild('reload', ReloadHandle())
