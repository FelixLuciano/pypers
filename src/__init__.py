import logging

import cssutils

from .Create import Create as create
from .Google import Google as google
from .Page import Page as page
from .Preview import Preview as preview
from .Send import Send as send
from .Workspace import Workspace as workspace


cssutils.ser.prefs.keepComments = False
cssutils.ser.prefs.lineSeparator = ""
cssutils.ser.prefs.propertyNameSpacer = ""

cssutils.log.setLevel(logging.CRITICAL)
