#coding:utf8

import json
from app.gate.local import login
from firefly.server.globalobject import rootserviceHandle, GlobalObject, masterserviceHandle
from app.gate.service.dispatcher import GateServiceHandle, dispatcher
from app.gate.model.usermanager import UserManager
from app.share.constants import *
from app.gate.util.loadbalance import GameRouter
from app.share.locale.i18n import L

@rootserviceHandle
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
            response['errno'] = E_NOT_LOGGED_IN
            response['errmsg'] = L('Not logged in')
            return json.dumps(response)

        # if user doesn't have a game node allocated, choose one
        if user.gameNode is None:
            serverName = GameRouter().pickLeastPressureServer()
            server = GameRouter().getServerByName(serverName)
            server.addClient(dynamicId)
            user.gameNode = serverName

        # now forward request to game node
        return GlobalObject().root.callChild(user.gameNode, key, dynamicId, data)

@rootserviceHandle
def pushObject(topicID, msg, sendList):
    """
    push something to client
    """
    GlobalObject().root.callChild("net", "pushObject", topicID, msg, sendList)

@rootserviceHandle
def onNetClientConnectionLost(dynamicId):
    print '##############################################'
    print '# client %d disconnected' % dynamicId
    print '##############################################'

    # drop user from some registry
    # extend the logic as you need
    user = UserManager().getUserByDynamicID(dynamicId)
    if user and user.gameNode:
        GameRouter().dropClient(user.gameNode, dynamicId)
        UserManager().dropUserByDynamicID(dynamicId)

@GateServiceHandle(COMMAND_LOGIN)
def loginToServer(key, dynamicId, request):
    # get user name and password
    args = json.loads(request)
    username = args.get('username')
    password = args.get('password')

    # login
    data = login.loginToServer(dynamicId, username, password)

    # construct response in json format and return
    response = {}
    response['errno'] = data.get('errno', E_UNKNOWN)
    if response['errno'] != E_OK:
        response['errmsg'] = data.get('errmsg')
    if data.has_key('data'):
        response['data'] = data['data']
    return json.dumps(response)

@masterserviceHandle
def getClientCount():
    return GameRouter().getAllClientCount()