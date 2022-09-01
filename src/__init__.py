if __name__ != "__main__":
    import logging
    import warnings

    import cssutils

    from .Page_file import Page_file
    from .Google import Google as google
    from .Page import Page as page
    from .Preview import Preview as preview
    from .Send import Send as send
    from .Workspace import Workspace as workspace


    warnings.simplefilter(action="ignore")

    cssutils.ser.prefs.keepComments = False
    cssutils.ser.prefs.lineSeparator = ""
    cssutils.ser.prefs.propertyNameSpacer = ""

    cssutils.log.setLevel(logging.CRITICAL)
