#coding:utf8

import json
from app.share.constants import *
from dispatcher import GameServiceHandle
from firefly.server.globalobject import masterServiceHandle, GlobalObject

@GameServiceHandle(COMMAND_TEST)
def testMethod(dynamicId, request):
    '''
    for test purpose, always return E_OK and a message in data
    '''

    # get message sent by client
    data = json.loads(request)
    msg = data['message']

    # return response
    reply = 'I got your message: %s' % msg
    response = {}
    response['errno'] = E_OK
    response['data'] = { 'message' : reply }
    return json.dumps(response)