import logging

import cssutils

from .Jupyter import Jupyter as jupyter
from .Page import Page as page
from .Preview import Preview as preview
from .Google import Google as google


cssutils.ser.prefs.keepComments = False
cssutils.ser.prefs.lineSeparator = u''
cssutils.ser.prefs.propertyNameSpacer = u''

cssutils.log.setLevel(logging.CRITICAL)
