#coding:utf8

import dataloader
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
GlobalObject().stophandler = doWhenStop

def loadModule():
    '''
    initial setup of db front
    '''
    mclient.flush_all()
    dataloader.registerMAdmin()
    dataloader.checkMemDB(1800)