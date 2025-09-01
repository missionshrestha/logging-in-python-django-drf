import logging

# Fixed-name logger
logger = logging.getLogger("simpleLogger")

def run_b():
    logger.info("Running from module B")
