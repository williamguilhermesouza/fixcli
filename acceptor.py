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

    def send_msg(self, msg):
        fix.Session.sendToTarget(msg, self.sessionID)

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        logger.debug(f"Created: {sessionID}")

    def onLogon(self, sessionID):
        logger.debug(f"Logon: {sessionID}")

    def onLogout(self, sessionID):
        logger.debug(f"Logout: {sessionID}")

    def toApp(self, message, sessionID):
        logger.debug(f'>App[{sessionID}]: {message}')

    def fromApp(self, message, sessionID):
        logger.debug(f'<App[{sessionID}]: {message}')

    def fromAdmin(self, message, sessionID):
        logger.debug(f'<Admin[{sessionID}]: {message}')

    def toAdmin(self, message, sessionID):
        logger.debug(f'>Admin[{sessionID}]: {message}')


        
