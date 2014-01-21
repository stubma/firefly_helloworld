#coding:utf8

from firefly.dbentrust.madminanager import MAdminManager
from twisted.internet import reactor
    
def checkMemDB(delta):
    '''
    check all data in memcache, sync it to table if necessary
    '''
    MAdminManager().checkAdmins()
    reactor.callLater(delta, checkMemDB, delta)
    

    
    
    
    