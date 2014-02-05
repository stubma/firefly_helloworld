#coding:utf8

import dataloader
from app.share.db import memtable
from firefly.dbentrust.madminanager import MAdminManager
from firefly.dbentrust.memclient import mclient
from firefly.server.globalobject import GlobalObject

def doWhenStop():
    '''
    invoked when server is stopped
    '''
    print "##################################################"
    print "# dbfront shutdown"
    print "##################################################"
    MAdminManager().checkAdmins()

# install stop handler
GlobalObject().stopHandler = doWhenStop

def loadModule():
    '''
    initial setup of db front
    '''
    mclient.flush_all()
    memtable.registerMAdmin()
    dataloader.checkMemDB(1800)