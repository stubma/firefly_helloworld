#coding:utf8

import json
from app.gate.local import login
from firefly.server.globalobject import rootServiceHandle, GlobalObject, masterServiceHandle
from app.gate.service.dispatcher import GateServiceHandle, dispatcher
from app.gate.model.usermanager import UserManager
from app.gate.util.loadbalance import GameRouter
from app.share.constants import *
from app.share.locale.i18n import L

@rootServiceHandle
def forwarding(key, dynamicId, data):
    """
    if a method is registered, forward it to local service
    if not, forward to game server
    """
    if dispatcher._targets.has_key(key):
        return dispatcher.callTarget(key, dynamicId, data)
    else:
        # find user model by dynamic id
        user = UserManager().getUserByDynamicID(dynamicId)
        if not user:
            response = {}
            response[KEY_ERRNO] = E_NOT_LOGGED_IN
            response[KEY_ERRMSG] = L('Not logged in')
            return json.dumps(response)

        # if user doesn't have a game node allocated, choose one
        if user.gameNode is None:
            serverName = GameRouter().pickLeastPressureServer()
            server = GameRouter().getServerByName(serverName)
            server.addClient(dynamicId)
            user.gameNode = serverName

        # now forward request to game node
        return GlobalObject().root.callChild(user.gameNode, key, dynamicId, data)

@rootServiceHandle
def pushObject(command, msg):
    """
    push something to client
    """
    GlobalObject().root.callChild("net", "pushObject", command, msg)

@rootServiceHandle
def onNetClientConnectionLost(dynamicId):
    print '##############################################'
    print '# client %d disconnected' % dynamicId
    print '##############################################'

    # drop user from some registry
    # extend the logic as you need
    user = UserManager().getUserByDynamicID(dynamicId)
    if user:
        UserManager().dropUserByDynamicID(dynamicId)
        if user.gameNode:
            GameRouter().dropClient(user.gameNode, dynamicId)

@GateServiceHandle(COMMAND_LOGIN)
def loginToServer(key, dynamicId, request):
    # get user name and password
    args = json.loads(request)
    username = args.get(KEY_USERNAME)
    password = args.get(KEY_PASSWORD)

    # login
    data = login.loginToServer(dynamicId, username, password)

    # construct response in json format and return
    response = {}
    response[KEY_ERRNO] = data.get(KEY_ERRNO, E_UNKNOWN)
    if response[KEY_ERRNO] != E_OK:
        response[KEY_ERRMSG] = data.get(KEY_ERRMSG)
    if data.has_key(KEY_DATA):
        response[KEY_DATA] = data[KEY_DATA]
    return json.dumps(response)

@masterServiceHandle
def getClientCount():
    return UserManager().getUserCount()