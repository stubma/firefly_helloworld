#coding:utf8

import json
from twisted.web.resource import *
from twisted.web.template import *
from twisted.web.static import File
from twisted.web.util import Redirect
from twisted.internet.defer import DeferredList
from twisted.python.filepath import *
from firefly.master.webapp import DefaultMasterDirectory
from firefly.server.globalobject import GlobalObject
from app.share.constants import *

class NetOperationsElement(Element):
    ''' net server operation sub template '''

    def __init__(self):
        super(NetOperationsElement, self).__init__(XMLFile(FilePath('webroot/net_operations.xml')))

class AdminElement(Element):
    ''' admin page template filler '''

    def __init__(self):
        super(AdminElement, self).__init__(XMLFile(FilePath('webroot/index.xml')))
        self.curRenderChildName = ''

    def onChildAllInfoCollected(self, result, tag, child):
        yield tag.clone().fillSlots(name = child._name,
                                    child_count = str(self.childCount))

    def onChildClientCountGot(self, result):
        if result is None:
            self.childCount = 0
        else:
            self.childCount = result

    @renderer
    def servers(self, request, tag):
        for child in GlobalObject().root.childsmanager._childs.values():
            # track current child name
            self.curRenderChildName = child._name

            # defer of get client count
            d1 = child.callbackChild('getClientCount')
            d1.addCallback(self.onChildClientCountGot)

            # create defer list
            dl = DeferredList([d1])

            # final callback
            dl.addCallback(self.onChildAllInfoCollected, tag, child)

            # return this defer list to fill one row
            yield dl

    @renderer
    def operations(self, request, tag):
        if self.curRenderChildName == 'net':
            yield NetOperationsElement()
        else:
            yield ''

class AdminHandle(Resource):
    ''' admin resource '''

    def render(self, request):
        return renderElement(request, AdminElement())

class MasterDirectory(DefaultMasterDirectory):
    '''
    custom web resource root for master web service
    '''

    def __init__(self):
        DefaultMasterDirectory.__init__(self)

        # add custom mapping
        GlobalObject().webroot.putChild('admin', AdminHandle())
        GlobalObject().webroot.putChild('static', File('webroot/static'))

    def getChild(self, path, request):
        # if path is do, means perform some action, and then refresh admin page
        if path == 'do':
            self.performAction(request)
            return Redirect('/')

        # by default, index.html or empty path redirect to admin
        if path is None or path == '' or path == 'index.html':
            return GlobalObject().webroot.getChildWithDefault('admin', request)

        # for other, just 404
        return DefaultMasterDirectory.getChild(self, path, request)

    def performAction(self, request):
        # get parameters
        action = request.args['action'][0]
        message = request.args['message'][0]
        node = request.args['node'][0]

        # perform action based on action parameter
        if action == 'push':
            child = GlobalObject().root.childsmanager.getChildByName(node)
            if child:
                msg = { KEY_ERRNO : E_OK, KEY_DATA : { KEY_MESSAGE : message } }
                child.callbackChild('pushObject', COMMAND_TEST_PUSH, json.dumps(msg))