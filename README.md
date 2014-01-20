What is it
==================
It is a skeleton project based on [firefly][1] game server framework. You can use it as:
* a start point of real game project
* a learning material of firefly
* a testbed of firefly-based game

It includes a cocos2d-x client to test the skeleton server. The client just connect the server and send a test command, and the server will return hello world.

How to Run Server
==================
To run the skeleton server:

1. install python 2.x. I use 2.7
2. install python libraries: twisted, mysqldb, memcached, zope.interface 
3. install JetBrains PyCharm
4. install mysql
5. install memcache
6. checkout [firefly][1], add it to python library
7. start memcached with ```memcached -p 11211 -d```, the memcache listening port is determined by config file
8. start mysql and execute init_db.sql, that will initialize databases
9. run ```python startmaster.py```

How to Run Client
===================
To run the client:

1. check out [cocos2d-x][2]
2. check out [cocos2dx-better][3]
3. cocos2d-x and cocos2dx-better should be in the same PARENT folder as firefly_helloworld. If not, you need fix reference and include path
4. open client iOS project with Xcode and just run it

[1]: https://github.com/9miao/firefly
[2]: https://github.com/cocos2d/cocos2d-x
[3]: https://github.com/stubma/cocos2dx-better
