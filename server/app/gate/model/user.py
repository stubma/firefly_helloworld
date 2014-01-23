#coding:utf8

from app.share.db import table_user

class User:
    '''
    user class
    '''

    def __init__(self, name, password, dynamicId = -1):
        self.id = 0
        self.name = name
        self.password = password
        self.dynamicId = dynamicId
        self.blocked = False
        self.gameNode = None
        self.initUser()
    
    def initUser(self):
        userInfo = table_user.getUserInfoByName(self.name)
        if not userInfo:
            self.blocked = True
            return
        self.blocked = userInfo['blocked']
        self.id = userInfo.get('id', 0)

    def getLoginExtraData(self):
        '''
        it returns a dict which will be returned to client when logged in
        '''
        extra = { 'id' : self.id }
        return extra
    
    def disconnectClient(self):
        pass
    
            