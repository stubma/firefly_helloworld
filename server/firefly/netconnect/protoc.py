#coding:utf8
'''
Created on 2011-9-20
登陆服务器协议
@author: lan (www.9miao.com)
'''
from twisted.internet import protocol,reactor
from twisted.python import log
from manager import ConnectionManager
from datapack import DataPackProtocol

def DefferedErrorHandle(e):
    '''延迟对象的错误处理'''
    log.err(str(e))
    return

class LiberateProtocol(protocol.Protocol):
    '''
    protocol between client and net front, a packet consist of header and body.
    body can be encrypted, and the encryption algorithm is described in header
    '''

    buff = ""
    
    def connectionMade(self):
        '''连接建立处理
        '''
        log.msg('Client %d login in.[%s,%d]'%(self.transport.sessionno,\
                self.transport.client[0],self.transport.client[1]))
        self.factory.connmanager.addConnection(self)
        self.factory.doConnectionMade(self)
        self.datahandler=self.dataHandleCoroutine()
        self.datahandler.next()
        
    def connectionLost(self,reason):
        '''连接断开处理
        '''
        log.msg('Client %d login out.'%(self.transport.sessionno))
        self.factory.doConnectionLost(self)
        self.factory.connmanager.dropConnectionByID(self.transport.sessionno)
        
    def safeToWriteData(self,data,command):
        '''线程安全的向客户端发送数据
        @param data: str 要向客户端写的数据
        '''
        if not self.transport.connected or data is None:
            return
        senddata = self.factory.produceResult(command, data)
        reactor.callFromThread(self.transport.write,senddata)
        
    def dataHandleCoroutine(self):
        """
        """
        length = self.factory.dataprotocol.getHeadLength()#获取协议头的长度
        while True:
            data = yield
            self.buff += data
            while self.buff.__len__() >= length:
                unpackdata = self.factory.dataprotocol.unpack(self.buff[:length])
                if not unpackdata.get('result'):
                    log.msg('illegal data package --')
                    self.transport.loseConnection()
                    break
                command = unpackdata.get('command')
                encryptAlgorithm = unpackdata.get('enc_alg')
                bodyLength = unpackdata.get('length')
                request = self.buff[length:length+bodyLength]

                # verify body length
                if request.__len__() < bodyLength:
                    log.msg('some data lose')
                    break

                # get body and push to factory
                self.buff = self.buff[length+bodyLength:]
                d = self.factory.doDataReceived(self, command, request, encryptAlgorithm)
                if not d:
                    continue
                d.addCallback(self.safeToWriteData,command)
                d.addErrback(DefferedErrorHandle)
        
    def dataReceived(self, data):
        '''数据到达处理
        @param data: str 客户端传送过来的数据
        '''
        self.datahandler.send(data)
            
class LiberateFactory(protocol.ServerFactory):
    '''协议工厂'''
    
    protocol = LiberateProtocol
    
    def __init__(self, dataprotocol=DataPackProtocol()):
        '''初始化
        '''
        self.service = None
        self.connmanager = ConnectionManager()
        self.dataprotocol = dataprotocol
        self.codec = None
        
    def setDataProtocol(self, dataprotocol):
        '''
        '''
        self.dataprotocol = dataprotocol
        
    def doConnectionMade(self, conn):
        '''当连接建立时的处理'''
        pass
    
    def doConnectionLost(self, conn):
        '''连接断开时的处理'''
        pass
    
    def addServiceChannel(self, service):
        '''添加服务通道'''
        self.service = service
    
    def doDataReceived(self, conn, commandID, data, encryptAlgorithm = 0):
        # verify and decode body
        decoded = data
        if self.codec:
            if not self.codec.verifyAlgorithm(commandID, encryptAlgorithm):
                log.msg('suspicious packet encrypt algorithm')
                return None
            decoded = self.codec.decode(data, encryptAlgorithm)

        # deliver
        defer_tool = self.service.callTarget(commandID, conn, decoded)
        return defer_tool
    
    def produceResult(self, command, response):
        '''
        generate packet can be directly sent through socket
        @param command: command id
        @param response: body string
        @return: binary packet to be sent
        '''

        # encode body
        encoded = response
        alg = 0
        if self.codec:
            alg = self.codec.selectAlgorithm(command, response)
            encoded = self.codec.encode(response, alg)

        return self.dataprotocol.pack(command, encoded, encryptAlgorithm = alg)
    
    def loseConnection(self, connID):
        """主动端口与客户端的连接
        """
        self.connmanager.loseConnection(connID)
    
    def pushObject(self, command, msg):
        '''
        server push a message to all clients, with given command
        @param command: command id
        @param msg: json body
        '''
        self.connmanager.pushObject(command, msg)

