#coding:utf8

from dispatcher import NetServiceHandle
from firefly.server.globalobject import GlobalObject, RemoteServiceHandle, masterserviceHandle
from app.share.constants import *

@NetServiceHandle(COMMAND_FORWARD)
def forwarding(keyname, conn, data):
    '''
    forward to gate node
    '''
    return GlobalObject().remote['gate'].callRemote("forwarding", keyname, conn.transport.sessionno, data)

# the decorator register this method in gate side
@RemoteServiceHandle('gate')
def pushObject(topicID, msg, sendList):
    '''
    push message to client connected to this net server
    '''
    GlobalObject().netfactory.pushObject(topicID, msg, sendList)

@masterserviceHandle
def getClientCount():
    return GlobalObject().netfactory.connmanager.getNowConnCnt()