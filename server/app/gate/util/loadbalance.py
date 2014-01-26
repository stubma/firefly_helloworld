#coding:utf8

from firefly.utils.singleton import Singleton
from firefly.server.globalobject import GlobalObject
from twisted.python import log

class GameServer(object):
    '''
    represent a game server node
    '''

    def __init__(self, name):
        self.name = name
        self.clients = set()

    def addClient(self, clientId):
        self.clients.add(clientId)

    def dropClient(self, clientId):
        self.clients.remove(clientId)

    def getClientCount(self):
        return len(self.clients)

class GameRouter(object):
    '''
    load balance component, allocate game server for client
    '''

    __metaclass__ = Singleton

    def __init__(self):
        self.servers = {}
        self.initServers()

    def initServers(self):
        for childName in GlobalObject().root.childsmanager._childs.keys():
            if "game" in childName:
                self.addServer(childName)

    def addServer(self, serverName):
        gs = GameServer(serverName)
        self.servers[serverName] = gs
        return gs

    def getServerByName(self, serverName):
        gs = self.servers.get(serverName)
        if not gs:
            gs = self.addServer(serverName)
        return gs

    def addClient(self, serverName, clientId):
        gs = self.getServerByName(serverName)
        if not gs:
            return False
        gs.addClient(clientId)
        return True

    def dropClient(self, serverName, clientId):
        gs = self.getServerByName(serverName)
        if gs:
            try:
                gs.dropClient(clientId)
            except Exception:
                msg = "error when serverName:%d drops clientId:%d" % (serverName, clientId)
                log.err(msg)

    def getAllClientCount(self):
        return sum([s.getClientCount() for s in self.servers.values()])

    def pickLeastPressureServer(self):
        '''
        choose a game server whose client count is least
        '''
        serverList = self.servers.values()
        sortedList = sorted(serverList, reverse = False, key = lambda s : s.getClientCount())
        if sortedList:
            return sortedList[0].name