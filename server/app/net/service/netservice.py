#coding:utf8

from dispatcher import NetServiceHandle
from firefly.server.globalobject import GlobalObject, RemoteServiceHandle, masterServiceHandle
from app.share.constants import *

@NetServiceHandle(COMMAND_FORWARD)
def forwarding(keyname, conn, data):
    '''
    forward to gate node
    '''
    return GlobalObject().remote['gate'].callRemote("forwarding", keyname, conn.transport.sessionno, data)

@RemoteServiceHandle('gate')
def pushObject(command, msg, sendList):
    '''
    push message to client connected to this net server
    '''
    GlobalObject().netfactory.pushObject(command, msg, sendList)

@masterServiceHandle
def getClientCount():
    return GlobalObject().netfactory.connmanager.getNowConnCnt()