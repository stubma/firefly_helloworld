#coding:utf8

from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService

# setup gate remote stub to game service
dispatcher = CommandService("gateremote")
GlobalObject().remote['gate']._reference.addService(dispatcher)

# decorator of game service api
class GameServiceHandle(object):
    def __init__(self, cmd):
        self.cmd = cmd

    def __call__(self, target):
        dispatcher.mapTarget(target, self.cmd)