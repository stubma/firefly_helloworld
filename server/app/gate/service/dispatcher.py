#coding:utf8

from firefly.utils.services import CommandService
from twisted.python import log
from twisted.internet import defer

class ServiceDispatcher(CommandService):
    def callTargetSingle(self, targetKey, *args, **kw):
        '''
        call method by method key, the method key is split from method name,
        so it acts as a dispatcher of remote calling
        '''
        self._lock.acquire()
        try:
            target = self.getTarget(targetKey)
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

# dispatcher instance
dispatcher = ServiceDispatcher('dispatcher')

# decorator of gate service api
class GateServiceHandle(object):
    def __init__(self, cmd):
        self.cmd = cmd

    def __call__(self, target):
        dispatcher.mapTarget(target, self.cmd)
