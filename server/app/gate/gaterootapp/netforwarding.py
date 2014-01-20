#coding:utf8

from firefly.server.globalobject import rootserviceHandle, GlobalObject
from app.gate.gateservice import localservice

@rootserviceHandle
def forwarding(key,dynamicId,data):
    """
    if a method is registered, forward it to local service
    """
    if localservice._targets.has_key(key):
        return localservice.callTarget(key,dynamicId,data)
    else:
        pass

@rootserviceHandle
def pushObject(topicID, msg, sendList):
    """
    push something to client
    """
    GlobalObject().root.callChild("net", "pushObject", topicID, msg, sendList)

@rootserviceHandle
def onNetClientConnectionLost(dynamicId):
    pass
