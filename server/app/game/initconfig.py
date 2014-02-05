#coding:utf8

from app.share.db import memtable
import reloaddata
from firefly.server.globalobject import GlobalObject

def doWhenStop():
    print '#############################################'
    print '# game server shutdown'
    print '#############################################'

# install stop handler
GlobalObject().stopHandler = doWhenStop

def loadModule():
    """
    init game server
    """
    reloaddata.loadConfigData()
    memtable.registerMAdmin()
    from service import *
