import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)  # -> 'shop.views' (inherits from 'shop')

def test_shop(request):
    logger.debug("shop.views: DEBUG log from test_shop()")
    logger.info("shop.views: INFO log from test_shop()")
    logger.error("shop.views: ERROR log from test_shop()")
    return HttpResponse("shop: check console, logs/shop.log, and logs/project_all.log")
