#coding:utf8

from dataloader import loadConfigData, registerMAdmin
from firefly.server.globalobject import GlobalObject

def doWhenStop():
    print '#############################################'
    print '# game server shutdown'
    print '#############################################'

# install stop handler
GlobalObject().stophandler = doWhenStop

def loadModule():
    """
    init game server
    """
    loadConfigData()
    registerMAdmin()
