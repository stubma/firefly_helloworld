#coding:utf8

from firefly.utils.services import CommandService
from twisted.python import log
from twisted.internet import defer

class LocalService(CommandService):
    def callTargetSingle(self, targetKey, *args, **kw):
        '''
        call method by method key, the method key is split from method name
        '''
        self._lock.acquire()
        try:
            target = self.getTarget(targetKey)
            if not target:
                log.err('the command ' + str(targetKey) + ' not Found on service')
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

# local service instance
localservice = LocalService('localservice')

def localserviceHandle(target):
    '''
    decorator of gate local service api
    '''
    localservice.mapTarget(target)
