# api/management/commands/nightly.py
from django.core.management.base import BaseCommand
from scoped_logging.decorators import scoped_function_log
from scoped_logging.context import get_logger

class Command(BaseCommand):
    help = "Run nightly jobs with scoped logging"

    @scoped_function_log("django-nightly-command")
    def handle(self, *args, **options):
        logger = get_logger(__name__)
        logger.info("🌙 Running nightly command...")
        # do work
        logger.info("✅ Nightly command finished!")
