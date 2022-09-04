if __name__ != "__main__":
    import logging
    import warnings

    import cssutils

    from .Google import Google as google
    from .Notebook import Notebook as notebook
    from .Page import Page as page
    from .Page_file import Page_file as page_file
    from .Parser import Parser as parser
    from .Preview import Preview as preview
    from .Preview_controls import Preview_controls as preview_controls
    from .Props import Props as props
    from .Send import Send as send
    from .Style import Style as style


    warnings.simplefilter(action="ignore")

    cssutils.ser.prefs.keepComments = False
    cssutils.ser.prefs.lineSeparator = ""
    cssutils.ser.prefs.propertyNameSpacer = ""

    cssutils.log.setLevel(logging.CRITICAL)

    def preview():
        preview.display()

    def send():
        send.display()
