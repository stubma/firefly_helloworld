#coding:utf8

from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService
from twisted.python import log
from twisted.internet import defer

class NetCommandService(CommandService):
    '''
    this service always forward invocation to gate node
    '''

    def callTargetSingle(self,targetKey,*args,**kw):
        self._lock.acquire()
        try:
            target = self.getTarget(0)
            if not target:
                log.err('the command '+str(targetKey)+' not Found on service')
                return None
            if targetKey not in self.unDisplay:
                log.msg("call method %s on service[single]"%target.__name__)
            defer_data = target(targetKey,*args,**kw)
            if not defer_data:
                return None
            if isinstance(defer_data,defer.Deferred):
                return defer_data
            d = defer.Deferred()
            d.callback(defer_data)
        finally:
            self._lock.release()
        return d

# create net service instance
netservice = NetCommandService("loginService")

def netserviceHandle(target):
    '''
    the decorator register method in service
    '''
    netservice.mapTarget(target)

# set service instance
GlobalObject().netfactory.addServiceChannel(netservice)

@netserviceHandle
def Forwarding_0(keyname,_conn,data):
    '''
    forward to gate node
    '''
    return GlobalObject().remote['gate'].callRemote("forwarding", keyname, _conn.transport.sessionno, data)
