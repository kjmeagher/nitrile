import logging
log = logging.getLogger(__name__)

Symbol = None

class Package(object):
    def __init__(self,options):
        log.info("Loading package {} with options {!r}"
                 .format(self.__class__.__name__,options))

