import logging
import sys
from app.utlis.config import get_configuration


def init_logger():
    conf = get_configuration()

    logging.basicConfig(
        level=getattr(logging, conf.LOG_LEVEL),
        format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d - %(funcName)s()] - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger("app")


logger = logging.getLogger("app")
