import quickfix as fix
import logging

logger = logging.getLogger(__name__)

class FixAcceptor(fix.Application):
    def __init__(self, settings_file):
        super().__init__()
        self.settings = fix.SessionSettings(settings_file)
        self.store = fix.FileStoreFactory(self.settings)
        self.log = fix.FileLogFactory(self.settings)
        self.engine = fix.SocketAcceptor(self, self.store, self.settings, self.log)

    def start(self):
        self.engine.start()

    def onCreate(self, sessionID):
        logger.info(f"created with session id {sessionID}")

    def onLogon(self, sessionID):
        logger.info(f"logged on with session id {sessionID}")

    def onLogout(self, sessionID):
        logger.info(f"logged out with session id {sessionID}")

    def toApp(self, message, sessionID):
        logger.info(f'message to app {message} on session id {sessionID}')

    def fromApp(self, message, sessionID):
        logger.info(f'message from app {message} on session id {sessionID}')

    def fromAdmin(self, message, sessionID): return
    def toAdmin(self, message, sessionID): return


        
