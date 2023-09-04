from pathlib import Path
import logging.config
import project
import yaml

configs = Path(project.__file__).parent.parent.parent / 'configs'
logger = logging.getLogger(__name__)


def setup_logging() -> None:
    with open(configs / "logging.yml") as file:
        logging_config = yaml.safe_load(file)
        logging.config.dictConfig(logging_config)
        logger.debug("Logging is successfully configured!")
