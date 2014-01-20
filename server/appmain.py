#coding:utf8

import sys

###########################################################
# remote debug setup, change to false if not in debug mode
###########################################################

if False:
    import pydevd
    args = sys.argv
    serverName = args[1]
    debugPorts = {
        'gate' : 30001,
        'dbfront' : 30002,
        'net' : 30000,
        'game1' : 30003
    }
    if debugPorts.has_key(serverName):
        pydevd.settrace('127.0.0.1', port = debugPorts[serverName], stdoutToServer = True, stderrToServer = True)

###########################################################
# remote debug setup end
###########################################################

import os
import json
from firefly.server.server import FFServer

# use epoll if not NT and POSIX
if os.name != 'nt' and os.name != 'posix':
    from twisted.internet import epollreactor
    epollreactor.install()

if __name__=="__main__":
    args = sys.argv
    serverName = None
    config = None

    # get server name and config path
    if len(args) > 2:
        serverName = args[1]
        config = json.load(open(args[2], 'r'))
    else:
        raise ValueError

    # get config block
    dbConfig = config.get('db')
    memConfig = config.get('memcached')
    serversConfig = config.get('servers', {})
    masterConfig = config.get('master', {})
    serverConfig = serversConfig.get(serverName)

    # ensure log file exists
    logPath = serverConfig.get('log')
    if logPath:
        f = open(logPath, 'w')
        f.close()

    # start a firefly server for given server name
    server = FFServer()
    server.config(serverConfig, dbconfig = dbConfig, memconfig = memConfig, masterconf = masterConfig)
    server.start()