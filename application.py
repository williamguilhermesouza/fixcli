import sys
import logging

from acceptor import FixAcceptor
from cli import Cli
from initiator import FixInitiator

logger = logging.getLogger(__name__)

class Application:
    def __init__(self, config):
        self.config = config
        self.cli = Cli()

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
                self.engine = self.start_initiator(self.config.settings_file)
            else:
                self.engine = self.start_acceptor(self.config.settings_file)

            self.engine.start()

            while True:
                message = self.cli.prompt_message()

            logging.info("Application shutting down...")

        except Exception as e:
            logging.exception("Unexpected error. Application interrupted.")

    def start_acceptor(self, settings_file):
        return FixAcceptor(settings_file)

    def start_initiator(self, settings_file):
        return FixInitiator(settings_file)




