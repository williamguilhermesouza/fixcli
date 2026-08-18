import sys
import logging
import threading

from fixcli.acceptor import FixAcceptor
from fixcli.cli import Cli
from fixcli.initiator import FixInitiator

logger = logging.getLogger(__name__)

'''TODO this may model better as a state machine
states: starting?, loging on, connected, logging out, stopping
events: to conn,   logged,    logout,    logged out,
actions:                    send,recv,  
'''

class Application:
    def __init__(self, config):
        self.config = config
        self.running = threading.Event()
        self.running.set()
        self.connected = threading.Event()
        self.cli = Cli(self.running, self.connected)

        logging.basicConfig(
            handlers=[logging.FileHandler("fixcli.log"), logging.StreamHandler(sys.stdout)],
            format="%(levelname)s %(asctime)s %(message)s",
            level=logging.DEBUG if self.config.verbose else logging.INFO,
        )

    def start(self):
        try:
            logging.info("Starting application...")
            logging.debug("Verbose mode enabled")

            self.engine = None
            if self.config.mode == 'initiator':
                self.engine = self.start_initiator(self.config.settings_file, self.connected)
            else:
                self.engine = self.start_acceptor(self.config.settings_file, self.connected)

            self.engine.start()
            self.connected.wait()

            while self.running.is_set() and self.connected.is_set():
                message = self.cli.prompt_message()
                if not message: continue
                self.engine.send_msg(message)

        except KeyboardInterrupt:
            logging.info("Application interrupted.")
        except Exception:
            logging.exception("Unexpected error. Application interrupted.")
        finally:
            logging.info("Application shutting down...")

            if self.engine:
                self.engine.stop()


    def start_acceptor(self, settings_file, connected_event):
        return FixAcceptor(settings_file, connected_event)

    def start_initiator(self, settings_file, connected_event):
        return FixInitiator(settings_file, connected_event)

