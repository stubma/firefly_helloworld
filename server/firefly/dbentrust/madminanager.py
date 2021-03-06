#coding:utf8
'''
Created on 2013-5-22

@author: lan (www.9miao.com)
'''
from firefly.utils.singleton import Singleton

class MAdminManager:
    __metaclass__ = Singleton
    
    def __init__(self):
        """
        """
        self.admins = {}
        
    def register(self,admin):
        """
        """
        self.admins[admin._name] = admin
        
    def dropAdmin(self,adminname):
        """
        """
        if self.admins.has_key(adminname):
            del self.admins[adminname]
    
    def getAdmin(self,adminname):
        """
        """
        return self.admins.get(adminname)
    
    def checkAdmins(self):
        """
        """
        for admin in self.admins.values():
            admin.checkAll()
    
    
    
        