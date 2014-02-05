#coding:utf8

from firefly.server.globalobject import GlobalObject
from firefly.netconnect.datapack import DataPackProtocol
from codec.packcodec import PackCodec

def onNetClientConnectionLost(conn):
    '''
    handle when connection lost, forward to gate node
    '''
    dynamicId = conn.transport.sessionno
    GlobalObject().remote['gate'].callRemote("onNetClientConnectionLost", dynamicId)

# setup the connection lost handler
GlobalObject().netFactory.doConnectionLost = onNetClientConnectionLost

# define the protocol which operates between client and net server
# the magic number is 'HELO', change it for your game
netProtocol = DataPackProtocol(ord('H'), ord('E'), ord('L'), ord('O'), 0, 0)
GlobalObject().netFactory.setDataProtocol(netProtocol)

# set packet codec
GlobalObject().netFactory.codec = PackCodec()

def loadModule():
    '''
    setup net server
    '''
    from service import *