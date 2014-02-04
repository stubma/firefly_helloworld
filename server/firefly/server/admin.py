#coding:utf8
'''
Created on 2013-8-12

@author: lan (www.9miao.com)
'''
from globalobject import GlobalObject,masterServiceHandle
from twisted.internet import reactor
from twisted.python import log

reactor = reactor


@masterServiceHandle
def stop():
    """
    """
    log.msg('stop')
    if GlobalObject().stophandler:
        GlobalObject().stophandler()
    reactor.callLater(0.5, reactor.stop)
    return True

@masterServiceHandle
def reload():
    """
    """
    log.msg('reload')
    if GlobalObject().reloadmodule:
        reload(GlobalObject().reloadmodule)
    return True

@masterServiceHandle
def remote_connect(rname, rhost):
    """
    """
    GlobalObject().remote_connect(rname, rhost)

