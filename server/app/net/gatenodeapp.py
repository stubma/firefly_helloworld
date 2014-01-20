#coding:utf8

from firefly.server.globalobject import GlobalObject, remoteserviceHandle

# the decorator register this method in gate side
@remoteserviceHandle('gate')
def pushObject(topicID, msg, sendList):
    '''
    push message to client connected to this net server
    '''
    GlobalObject().netfactory.pushObject(topicID, msg, sendList)