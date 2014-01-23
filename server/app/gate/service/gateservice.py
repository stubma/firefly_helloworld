#coding:utf8

import json
from app.gate.local import login
from firefly.server.globalobject import rootserviceHandle, GlobalObject
from app.gate.service.dispatcher import GateServiceHandle, dispatcher
from app.gate.model.usermanager import UserManager
from app.share.constants import *

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
            return


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

    # drop user from manager
    # extend the logic as you need
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
