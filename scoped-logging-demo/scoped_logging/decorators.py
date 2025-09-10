# scoped-logging-demo/scoped_logging/decorators.py
from __future__ import annotations
import functools
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Generator
from .context import start_scope, end_scope, get_logger, safe_filename

BASE_DIR = Path("logs")

@contextmanager
def function_log_scope(label: str) -> Generator[None, None, None]:
    start_scope("function", BASE_DIR, safe_filename(label), reuse_if_exists=True)
    logger = get_logger("function")
    logger.info(f"🔧 Function scope start: {label}")
    try:
        yield
    except Exception:
        logger.exception("💥 Exception inside function scope")
        raise
    finally:
        logger.info("🔚 Function scope end")
        end_scope()

def scoped_function_log(label: str | None = None):
    def outer(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            human = label or func.__name__
            with function_log_scope(human):
                logger = get_logger(func.__module__)
                logger.info(f"▶️ {func.__name__} called")
                return func(*args, **kwargs)
        return wrapper
    return outer
