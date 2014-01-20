#coding:utf8

from firefly.dbentrust.mmode import MAdmin
from firefly.dbentrust.madminanager import MAdminManager
from twisted.internet import reactor

# reactor
reactor = reactor

# table admin definition
# add your table here!
messageMAdmin = MAdmin('message', 'id', incrkey='id')
messageMAdmin.insert()

def registerMAdmin():
    '''
    register database table to memcached
    '''
    MAdminManager().registe(messageMAdmin)
    
def checkMemDB(delta):
    '''
    check all data in memcache, sync it to table if necessary
    '''
    MAdminManager().checkAdmins()
    reactor.callLater(delta, checkMemDB, delta)
    

    
    
    
    