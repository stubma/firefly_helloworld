#coding:utf8

from twisted.web.resource import *
from twisted.web.template import *
from twisted.web.static import File
from twisted.internet.defer import DeferredList
from twisted.python.filepath import *
from firefly.master.webapp import DefaultMasterDirectory
from firefly.server.globalobject import GlobalObject

class AdminElement(Element):
    ''' admin page template filler '''

    def __init__(self):
        super(AdminElement, self).__init__(XMLFile(FilePath('webroot/index.xml')))

    def onChildAllInfoCollected(self, result, tag, child):
        yield tag.clone().fillSlots(name = child._name,
                                    child_count = str(self.childCount),
                                    operations = '')

    def onChildClientCountGot(self, result):
        if result is None:
            self.childCount = 0
        else:
            self.childCount = result

    @renderer
    def servers(self, request, tag):
        for child in GlobalObject().root.childsmanager._childs.values():
            # defer of get client count
            d1 = child.callbackChild('getClientCount')
            d1.addCallback(self.onChildClientCountGot)

            # create defer list
            dl = DeferredList([d1])

            # final callback
            dl.addCallback(self.onChildAllInfoCollected, tag, child)

            # return this defer list to fill one row
            yield dl

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
        # by default, index.html or empty path redirect to admin
        if path is None or path == '' or path == 'index.html':
            return GlobalObject().webroot.getChildWithDefault('admin', request)

        # for other, just 404
        return DefaultMasterDirectory.getChild(self, path, request)