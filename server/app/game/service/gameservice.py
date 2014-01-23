#coding:utf8

import json
from app.share.constants import *
from dispatcher import GameServiceHandle

@GameServiceHandle(COMMAND_TEST)
def testMethod(dynamicId, request):
    data = json.loads(request)
    msg = data['message']
    print msg