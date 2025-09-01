import logging
from django.http import HttpResponse

logger = logging.getLogger('django')

def test_view(request):
    logger.debug("DEBUG: hello from test_view()")
    logger.info("INFO: This is an info log from a Django view")
    logger.error("ERROR: This is an error log from a Django view")
    return HttpResponse("Check your logs!")