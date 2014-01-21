#coding:utf8

from firefly.server.globalobject import GlobalObject
from firefly.netconnect.datapack import DataPackProtoc

def onNetClientConnectionLost(conn):
    '''
    handle when connection lost, forward to gate node
    '''
    dynamicId = conn.transport.sessionno
    GlobalObject().remote['gate'].callRemote("onNetClientConnectionLost", dynamicId)

# setup the connection lost handler
GlobalObject().netfactory.doConnectionLost = onNetClientConnectionLost

# define the protocol which operates between client and net server
dataprotocl = DataPackProtoc(78, 37, 38, 48, 0, 0)
GlobalObject().netfactory.setDataProtocl(dataprotocl)

def loadModule():
    '''
    setup net server
    '''
    import netapp
    import gatenodeapp