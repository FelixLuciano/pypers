import logging

import cssutils

from .Google import Google as google
from .Jupyter import Jupyter as jupyter
from .Page import Page as page
from .Preview import Preview as preview


cssutils.ser.prefs.keepComments = False
cssutils.ser.prefs.lineSeparator = ""
cssutils.ser.prefs.propertyNameSpacer = ""

cssutils.log.setLevel(logging.CRITICAL)
