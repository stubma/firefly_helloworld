#coding:utf8
'''
Created on 2013-8-2

@author: lan (www.9miao.com)
'''
from firefly.utils.singleton import Singleton

class GlobalObject:
    
    __metaclass__ = Singleton
    
    def __init__(self):
        self.netFactory = None#net前端
        self.root = None#分布式root节点
        self.remote = {}#remote节点
        self.db = None
        self.stopHandler = None
        self.webroot = None
        self.masterRemote = None
        self.reloadmodule = None
        self.remote_connect = None
        self.json_config = {}
        self.remote_map = {}
        
    def config(self,netFactory=None,root = None,remote=None,db=None):
        self.netFactory = netFactory
        self.root = root
        self.remote = remote
        self.db = db
        
def masterServiceHandle(target):
    """
    """
    GlobalObject().masterRemote._reference._service.mapTarget(target)
        
def netserviceHandle(target):
    """
    """
    GlobalObject().netFactory.service.mapTarget(target)
        
def rootServiceHandle(target):
    """
    """
    GlobalObject().root.service.mapTarget(target)

# decorator of web service
class WebServiceHandle:
    def __init__(self,url=None):
        self._url = url
        
    def __call__(self,cls):
        if self._url:
            GlobalObject().webroot.putChild(self._url, cls())
        else:
            GlobalObject().webroot.putChild(cls.__name__, cls())

# decorator of remote peer api
class RemoteServiceHandle:
    def __init__(self,remotename):
        self.remotename = remotename
        
    def __call__(self,target):
        GlobalObject().remote[self.remotename]._reference._service.mapTarget(target)
        
