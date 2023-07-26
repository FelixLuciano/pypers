if __name__ != "__main__":
    import logging
    import warnings

    import cssutils

    from .Google import Google
    from .Notebook import Notebook
    from .Page import Page
    from .Page_file import Page_file
    from .Parser import Parser
    from .Preview import Preview
    from .Preview_controls import Preview_controls
    from .Props import Props
    from .Send import Send
    from .Send_controls import Send_controls
    from .Style import Style
    from .User_prop import User_prop


    warnings.simplefilter(action="ignore")

    cssutils.ser.prefs.keepComments = False
    cssutils.ser.prefs.lineSeparator = ""
    cssutils.ser.prefs.propertyNameSpacer = ""

    cssutils.log.setLevel(logging.CRITICAL)

    define_user_prop = User_prop.define_decorator

    def preview():
        Preview.display()

    def send():
        Send.display()
