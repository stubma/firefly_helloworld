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
    deviceId = args.get(KEY_DEVICE_ID)

    # login
    data = login.loginToServer(dynamicId, username, password, deviceId)

    # construct response in json format and return
    response = {}
    response[KEY_ERRNO] = data.get(KEY_ERRNO, E_UNKNOWN)
    if response[KEY_ERRNO] != E_OK:
        response[KEY_ERRMSG] = data.get(KEY_ERRMSG)
    if data.has_key(KEY_DATA):
        response[KEY_DATA] = data[KEY_DATA]
    return json.dumps(response)

@GateServiceHandle(COMMAND_QUERY_BIND)
def queryBind(key, dynamicId, request):
    # get device id
    args = json.loads(request)
    deviceId = args.get(KEY_DEVICE_ID)

    # query bind
    data = login.queryBind(dynamicId, deviceId)

    # construct response
    response = {}
    response[KEY_ERRNO] = data.get(KEY_ERRNO, E_UNKNOWN)
    if data.has_key(KEY_DATA):
        response[KEY_DATA] = data[KEY_DATA]
    return json.dumps(response)

@masterServiceHandle
def getClientCount():
    return UserManager().getUserCount()

@masterServiceHandle
def getUserNames():
    '''
    get a name list of all logged user
    @return: a list of name string
    '''
    return [u.name for u in UserManager().users.values()]

@masterServiceHandle
def pushObject(command, msg, users=[]):
    '''
    push message to clients
    @param command: command id
    @param msg: message string
    @param users: user name list to who the message will be pushed, if emtpy, push to all clients
    '''
    sendList = [UserManager().getDynamicIDByName(name) for name in users]
    GlobalObject().root.callChild("net", "pushObject", command, msg, sendList)