#coding:utf8

from dispatcher import netserviceHandle
from firefly.server.globalobject import GlobalObject, remoteserviceHandle

@netserviceHandle
def forwarding_0(keyname, conn, data):
    '''
    forward to gate node
    '''
    return GlobalObject().remote['gate'].callRemote("forwarding", keyname, conn.transport.sessionno, data)

# the decorator register this method in gate side
@remoteserviceHandle('gate')
def pushObject(topicID, msg, sendList):
    '''
    push message to client connected to this net server
    '''
    GlobalObject().netfactory.pushObject(topicID, msg, sendList)