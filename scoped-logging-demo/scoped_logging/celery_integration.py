# scoped-logging-demo/scoped_logging/celery_integration.py
from __future__ import annotations
from pathlib import Path
from celery import signals
from .context import start_scope, end_scope, get_logger, safe_filename

BASE_DIR = Path("logs")

@signals.task_prerun.connect
def _task_prerun(sender=None, task_id=None, task=None, args=None, kwargs=None, **extras):
    label = f"{sender.name or 'celery_task'}"
    start_scope("task", BASE_DIR, safe_filename(label), reuse_if_exists=True)
    get_logger("celery").info(f"🚚 Task start: {label} id={task_id}")

@signals.task_postrun.connect
def _task_postrun(sender=None, task_id=None, task=None, args=None, kwargs=None, retval=None, state=None, **extras):
    logger = get_logger("celery")
    logger.info(f"🏁 Task end: {sender.name if sender else '?'} id={task_id} state={state}")
    end_scope()
