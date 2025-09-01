import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def test_core(request):
    logger.debug("core.views: DEBUG log from test_core()")
    logger.info("core.views: INFO log from test_core()")
    logger.warning("core.views: WARNING log from test_core()")
    return HttpResponse("core: check console, logs/core.log, and logs/project_all.log")