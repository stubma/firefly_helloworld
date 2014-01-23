#coding:utf8

import json
from app.gate.local import login
from firefly.server.globalobject import rootserviceHandle, GlobalObject
from app.gate.service.dispatcher import gateserviceHandle, dispatcher
from app.gate.model.usermanager import UserManager
from app.share.constants import *

@rootserviceHandle
def forwarding(key, dynamicId, data):
    """
    if a method is registered, forward it to local service
    """
    if dispatcher._targets.has_key(key):
        return dispatcher.callTarget(key, dynamicId, data)
    else:
        pass

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

@gateserviceHandle
def loginToServer_101(key, dynamicId, request):
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
