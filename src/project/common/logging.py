import logging.config

import yaml

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    with open('logging.yml') as file:
        logging_config = yaml.safe_load(file)
        logging.config.dictConfig(logging_config)
        logger.debug("Logging is successfully configured!")
