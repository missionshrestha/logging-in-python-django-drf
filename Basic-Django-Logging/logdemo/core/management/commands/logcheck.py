import logging
from django.core.management.base import BaseCommand

core_logger = logging.getLogger('core')
shop_logger = logging.getLogger('shop')
django_logger = logging.getLogger('django')

class Command(BaseCommand):
    help = "Emit sample logs from a management command to verify logger config."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Running logcheck..."))

        core_logger.debug("core: debug from management command")
        core_logger.info("core: info from management command")

        shop_logger.warning("shop: warning from management command")
        shop_logger.error("shop: error from management command")

        django_logger.info("django: info from management command (framework-level logger)")

        try:
            1 / 0
        except ZeroDivisionError:
            # .exception logs ERROR + traceback when called in an except block
            core_logger.exception("core: exception captured with stacktrace")

        self.stdout.write(self.style.SUCCESS("Done. Check logs/core.log, logs/shop.log, logs/project_all.log"))
