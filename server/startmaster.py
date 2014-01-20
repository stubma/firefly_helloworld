#coding:utf8

import os
from firefly.master.master import Master

# if not NT and POSIX, use epoll
if os.name != "nt" and os.name != "posix":
    from twisted.internet import epollreactor
    epollreactor.install()

# start master, master will read config and start other server in subprocess
if __name__ == "__main__":
    master = Master()
    master.config("config.json", "appmain.py")
    master.start()
    
    