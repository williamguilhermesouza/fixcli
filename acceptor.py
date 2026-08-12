import quickfix as fix

class FixAcceptor(fix.Application):
    def onCreate(self, sessionID):
        print(f"created with session id {sessionID}")
    def onLogon(self, sessionID):
        print(f"logged on with session id {sessionID}")
    def onLogout(self, sessionID): return
    def toAdmin(self, message, sessionID): return
    def toApp(self, message, sessionID):
        print(f'message to app {message} on session id {sessionID}')
    def fromAdmin(self, message, sessionID): return
    def fromApp(self, message, sessionID): return
        print(f'message from app {message} on session id {sessionID}')

        
