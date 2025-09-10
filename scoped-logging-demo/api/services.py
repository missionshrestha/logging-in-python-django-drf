# scoped-logging-demo/api/services.py
from .utils import heavy_compute
from scoped_logging.context import get_logger
from scoped_logging.redact import redact

def greet(name: str, headers: dict) -> str:
    logger = get_logger(__name__)
    logger.debug("service.greet: entering")
    logger.info("service.greet: headers=%s", redact(str(dict(headers))))
    msg = f"Hello, {name}!"
    logger.info("service.greet: built message=%r", msg)
    heavy = heavy_compute(len(name))
    logger.info("service.greet: heavy result=%s", heavy)
    logger.debug("service.greet: exiting")
    return msg
