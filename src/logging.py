import logging.config
import yaml

from src.settings import CONFIG_DIR


def setup_logging(log_level: str):
    config_file = CONFIG_DIR / "logging.yaml"
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)

    for logger_name in ["__main__", "src"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
