import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


# the __name__ resolve to "uicheckapp.services"
logger = logging.getLogger(__name__)
# This will load the uicheckapp logger


class EchoService:
    def echo(self, msg):
        logger.info("echoing something from the uicheckapp logger")
        print(msg)
