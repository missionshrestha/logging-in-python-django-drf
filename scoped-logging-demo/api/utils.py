# scoped-logging-demo/api/utils.py
import time
from scoped_logging.context import get_logger

def heavy_compute(n: int) -> int:
    logger = get_logger(__name__)
    logger.debug("utils.heavy_compute: start n=%s", n)
    time.sleep(0.05)
    val = sum(range(n * 1000))
    logger.debug("utils.heavy_compute: done val=%s", val)
    return val
