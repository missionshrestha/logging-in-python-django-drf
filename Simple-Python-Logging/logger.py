import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

logger.debug("This is a DEBUG log")       # diagnostic info, very verbose
logger.info("This is an INFO log")        # general app flow info
logger.warning("This is a WARNING log")   # something unexpected, but still working
logger.error("This is an ERROR log")      # a serious problem, but app keeps running
logger.critical("This is a CRITICAL log") # very serious error, app may not continue
