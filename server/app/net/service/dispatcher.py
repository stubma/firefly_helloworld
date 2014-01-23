#coding:utf8

from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService
from twisted.python import log
from twisted.internet import defer

class ServiceDispatcher(CommandService):
    '''
    Dispatcher of client command, it always forward client invocation to gate server
    '''

    def callTargetSingle(self,targetKey,*args,**kw):
        self._lock.acquire()
        try:
            target = self.getTarget(0)
            if not target:
                log.err('the command ' + str(targetKey) + ' not found on service')
                return None
            if targetKey not in self.unDisplay:
                log.msg("call method %s on service[single]" % target.__name__)
            defer_data = target(targetKey, *args, **kw)
            if not defer_data:
                return None
            if isinstance(defer_data, defer.Deferred):
                return defer_data
            d = defer.Deferred()
            d.callback(defer_data)
        finally:
            self._lock.release()
        return d

# create dispatcher instance and set it
dispatcher = ServiceDispatcher("dispatcher")
GlobalObject().netfactory.addServiceChannel(dispatcher)

# decorator of net service api
class NetServiceHandle(object):
    def __init__(self, cmd):
        self.cmd = cmd

    def __call__(self, target):
        dispatcher.mapTarget(target, self.cmd)
