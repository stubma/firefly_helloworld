What is it
==================
It is a skeleton project based on [firefly][1] game server framework. You can use it as:
* A start point of real game project
* A learning material of firefly
* A testbed of firefly-based game

It includes a cocos2d-x client to test the skeleton server. The client just connect the server and send a test command, and the server will return hello world.

How to Run Server
==================
To run the skeleton server:

1. Install python 2.x. I use 2.7
2. Install python libraries: twisted, MySQL-python, python-memcache, zope.interface, affinity, DBUtils
3. Install JetBrains PyCharm (if you use IDE)
4. Install mysql, set root password to 123456. If you want use different username or password, change config.json
5. Install memcache
6. Start memcached with ```memcached -p 11211 -d```, the memcache listening port is determined by config file
7. Start mysql and execute init_db.sql, that will initialize databases
8. Run ```python startmaster.py```

For customization purpose, I include firefly source code in project. So no need to clone firefly.

How to Run Client
===================
To run the client:

1. Check out [cocos2d-x][2]
2. Check out [cocos2dx-better][3]
3. cocos2d-x and cocos2dx-better should be in the same PARENT folder as firefly_helloworld. If not, you need fix reference and include path
4. Open client iOS project with Xcode and just run it

Admin Portal
===================
Here is a web admin portal can be accessed from http://localhost:10002, the port is configured in config.json and you can change it. The web admin portal uses twisted template, it looks ugly but a good start point to implement your own portal.

Basic
====================
Firefly is a python game server framework. Generally it has six components:

* A memory cache client, such as memcached. The memory cache client is shared by other components
* A database front which is shared by other components
* Network front, which accepts client connections and forward all invocations to gate server. Of course you can do something more than forwarding as long as you think it is necessary
* Gate server acts as a central dispatcher for client requests. You can add general logic, which means same to all clients, to gate server, such as login, logout, etc.
* Game server holds all game-specific logic and receives request from gate server. Game server can have more than one instance so that the overload can be balanced. 
* Master node. Generally it does nothing, but I think it is a good place to install monitor and maintenance tools on it. I will try this in helloworld project

Basically, db front, network, gate and game are sub node of master. Meanwhile, db front, network and game are sub node of gate. They are connected by twisted RPC, which is bidirectional, so they can call each other. That is the way how they interact.

However, above is just a reference structure. It should not the only one and not mandatory. The way you build your game server could be different, but this helloworld project will follow this structure. 

[1]: https://github.com/9miao/firefly
[2]: https://github.com/cocos2d/cocos2d-x
[3]: https://github.com/stubma/cocos2dx-better
