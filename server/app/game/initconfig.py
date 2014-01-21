#coding:utf8

from app.share.db import memtable
import dataloader
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
    dataloader.loadConfigData()
    memtable.registerMAdmin()
