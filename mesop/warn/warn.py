import logging

logger = logging.getLogger(__name__)


def warn(message: str) -> None:
  logger.warning("\033[93m[warning]\033[0m " + message)
