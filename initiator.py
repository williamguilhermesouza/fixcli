import quickfix as fix
import logging
import time

logger = logging.getLogger(__name__)

class FixInitiator(fix.Application):
    def __init__(self, settings_file, connected_event):
        super().__init__()
        self.connected = connected_event
        self.settings = fix.SessionSettings(settings_file)
        self.store = fix.FileStoreFactory(self.settings)
        self.log = fix.FileLogFactory(self.settings)
        self.engine = fix.SocketInitiator(self, self.store, self.settings, self.log)

    def start(self):
        self.engine.start()
    def stop(self):
        self.engine.stop()

    def send_test_msg(self):

        logger.info("Trying to send test message...")

        if not self.sessionID:
            logger.error('trying to send test message without creating')
            return

        msg = fix.Message()
        msg.setField(fix.TestReqID("TEST"))
        header = msg.getHeader()
        header.setField(fix.BeginString("FIX.4.4"))
        header.setField(fix.MsgType(fix.MsgType_TestRequest))

        fix.Session.sendToTarget(msg, self.sessionID)

        logger.info("Test message sent.")

    def send_msg(self, msg):
        fix.Session.sendToTarget(msg, self.sessionID)

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        logger.debug(f"Created: {sessionID}")

    def onLogon(self, sessionID):
        logger.debug(f"Logon: {sessionID}")
        self.connected.set()

    def onLogout(self, sessionID):
        logger.debug(f"Logout: {sessionID}")
        self.connected.clear()

    def toApp(self, message, sessionID):
        logger.debug(f'>App[{sessionID}]: {message}')

    def fromApp(self, message, sessionID):
        logger.debug(f'<App[{sessionID}]: {message}')

    def fromAdmin(self, message, sessionID):
        logger.debug(f'<Admin[{sessionID}]: {message}')

    def toAdmin(self, message, sessionID):
        logger.debug(f'>Admin[{sessionID}]: {message}')

        
