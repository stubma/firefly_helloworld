#coding:utf8

import json
from app.gate.local import login
from firefly.server.globalobject import rootserviceHandle, GlobalObject
from app.gate.service.dispatcher import gateserviceHandle, dispatcher

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

@gateserviceHandle
def loginToServer_101(key, dynamicId, request_proto):
    # get user name and password
    args = json.loads(request_proto)
    username = args.get('username')
    password = args.get('password')

    # login
    data = login.loginToServer(dynamicId, username, password)

    # construct response in json format and return
    response = {}
    response['result'] = data.get('result', False)
    response['data'] = data['data']
    print json.dumps(response)
    return json.dumps(response)
