#coding:utf8

import os
import locale
import gettext

# get current language code
_tuple = locale.getdefaultlocale()
lan = 'en'
if _tuple[0] is not None:
    lan = _tuple[0][:2]

# load strings
L = gettext.translation('strings', localedir = os.path.dirname(__file__), languages = [lan]).ugettext