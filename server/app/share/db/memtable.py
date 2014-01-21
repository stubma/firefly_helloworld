#coding:utf8

from firefly.dbentrust.mmode import MAdmin
from firefly.dbentrust.madminanager import MAdminManager

# table admin definition
# add your tables which is need to be cached
messageMAdmin = MAdmin('message', 'id', incrkey = 'id')
messageMAdmin.insert()

def registerMAdmin():
    '''
    connect table and memory cache
    '''
    MAdminManager().registe(messageMAdmin)