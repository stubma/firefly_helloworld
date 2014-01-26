#coding:utf8

from twisted.web.resource import *
from twisted.web.template import *
from twisted.python.filepath import *
from firefly.master.webapp import DefaultMasterDirectory
from firefly.server.globalobject import GlobalObject

class AdminElement(Element):
    ''' admin page template filler '''

    loader = XMLFile(FilePath('webroot/index.xml'))

    @renderer
    def header(self, request, tag):
        return tag('Header')

    @renderer
    def footer(self, request, tag):
        return tag('Footer')

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

    def getChild(self, path, request):
        # by default, index.html or empty path redirect to admin
        if path is None or path == '' or path == 'index.html':
            return GlobalObject().webroot.getChildWithDefault('admin', request)

        # for other, just 404
        return DefaultMasterDirectory.getChild(path, request)