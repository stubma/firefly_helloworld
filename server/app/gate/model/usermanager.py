#coding:utf8

from firefly.utils.singleton import Singleton

class UserManager:
    '''
    General purpose user manager, singleton
    '''
    
    __metaclass__ = Singleton

    def __init__(self):
        self.users = {}
        
    def addUser(self, user):
        if self.users.has_key(user.id):
            self.users[user.id].disconnectClient()
            self.dropUserByID(user.id)
        self.users[user.id] = user

    def getUserByID(self, uid):
        return self.users.get(uid)
        
    def getUserByDynamicID(self, dynamicId):
        for user in self.users.values():
            if user.dynamicId == dynamicId:
                return user
        return None

    def getUserByName(self, username):
        for k in self.users.values():
            if k.getName() == username:
                return k
        return None

    def dropUser(self, user):
        userId = user.id
        try:
            del self.users[userId]
        except Exception, e:
            print e
            
    def dropUserByDynamicID(self, dynamicId):
        user = self.getUserByDynamicID(dynamicId)
        if user:
            self.dropUser(user)

    def dropUserByID(self, userId):
        user = self.getUserByID(userId)
        if user:
            self.dropUser(user)
