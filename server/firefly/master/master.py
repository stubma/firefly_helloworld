#coding:utf8
'''
Created on 2013-8-2

@author: lan (www.9miao.com)
'''
import subprocess,json,sys
from twisted.internet import reactor
from firefly.utils import  services
from firefly.distributed.root import PBRoot,BilateralFactory
from firefly.server.globalobject import GlobalObject
from twisted.web import vhost
from firefly.web.delayrequest import DelaySite
from twisted.python import log
from firefly.server.logobj import loogoo
from webapp import DefaultMasterDirectory

reactor = reactor

MULTI_SERVER_MODE = 1
SINGLE_SERVER_MODE = 2
MASTER_SERVER_MODE = 3



class Master:
    """
    """
    
    def __init__(self):
        """
        """
        self.configpath = None
        self.mainpath = None
        self.root = None
        self.webroot = None
        
    def config(self,configpath,mainpath):
        """
        """
        self.configpath = configpath
        self.mainpath = mainpath
        
    def masterapp(self):
        # get config
        config = json.load(open(self.configpath,'r'))
        GlobalObject().json_config = config
        mastercnf = config.get('master')
        rootport = mastercnf.get('rootport')
        webport = mastercnf.get('webport')
        masterlog = mastercnf.get('log')
        webroot = mastercnf.get('webroot')

        # create root and webroot
        self.root = PBRoot()
        rootservice = services.Service("rootservice")
        self.root.addServiceChannel(rootservice)
        self.webroot = vhost.NameVirtualHost()

        # save root and webroot to global
        GlobalObject().root = self.root
        GlobalObject().webroot = self.webroot

        # add root resource, the webroot can be customized
        if webroot:
            parts = webroot.split('.')
            cls = parts[-1]
            pkg = '.'.join(parts[0:-1])
            module = __import__(pkg, fromlist = [cls])
            clsObj = getattr(module, cls)
            self.webroot.addHost('localhost', clsObj())
        else:
            self.webroot.addHost('localhost', DefaultMasterDirectory())

        if masterlog:
            log.addObserver(loogoo(masterlog))#日志处理
        log.startLogging(sys.stdout)
        import rootapp
        reactor.listenTCP(webport, DelaySite(self.webroot))
        reactor.listenTCP(rootport, BilateralFactory(self.root))
        
    def start(self):
        '''
        '''
        sys_args = sys.argv
        if len(sys_args)>2 and sys_args[1] == "single":
            server_name = sys_args[2]
            if server_name == "master":
                mode = MASTER_SERVER_MODE
            else:
                mode = SINGLE_SERVER_MODE
        else:
            mode = MULTI_SERVER_MODE
            server_name = ""
            
        if mode == MULTI_SERVER_MODE:
            self.masterapp()
            config = json.load(open(self.configpath,'r'))
            sersconf = config.get('servers')
            for sername in sersconf.keys():
                cmds = 'python %s %s %s'%(self.mainpath,sername,self.configpath)
                subprocess.Popen(cmds,shell=True)
            reactor.run()
        elif mode == SINGLE_SERVER_MODE:
            config = json.load(open(self.configpath,'r'))
            sername = server_name
            cmds = 'python %s %s %s'%(self.mainpath,sername,self.configpath)
            subprocess.Popen(cmds,shell=True)
        else:
            self.masterapp()
            reactor.run()
            
            
