# scoped-logging-demo/scoped_logging/context.py
from __future__ import annotations
import logging, re, socket, threading, uuid
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Literal, List

# -------- Context --------
trace_id_var: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)
_scope_stack_var: ContextVar[List[Literal["request", "function", "task"]]] = ContextVar(
    "scope_stack", default=[]
)
handler_owner_var: ContextVar[bool] = ContextVar("handler_owner", default=False)
current_handler_var: ContextVar[Optional[logging.Handler]] = ContextVar("current_handler", default=None)

_handler_lock = threading.RLock()

# -------- Helpers --------
def now_ms_str() -> str:
    dt = datetime.now()
    return dt.strftime("%Y-%m-%d_%H-%M-%S.") + f"{int(dt.microsecond/1000):03d}"

def safe_filename(part: str) -> str:
    part = (part or "log").strip().replace(" ", "_")
    return re.sub(r"[^A-Za-z0-9._-]+", "-", part)[:200] or "log"

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def _scope_type_current() -> str:
    stack = _scope_stack_var.get()
    return stack[-1] if stack else "-"

# -------- Filter --------
class TraceContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = trace_id_var.get() or "-"
        record.scope_type = _scope_type_current()
        record.hostname = socket.gethostname()
        return True

# -------- Attach / Detach --------
@dataclass
class ScopeInfo:
    trace_id: str
    scope_type: Literal["request", "function", "task"]
    logfile_path: Path

def _attach_file_handler(base_logger_name: str, logfile_path: Path) -> logging.Handler:
    with _handler_lock:
        handler = logging.FileHandler(logfile_path, encoding="utf-8")
        fmt = logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d | %(levelname)-8s | %(trace_id)s | %(scope_type)s "
                "| %(name)s:%(funcName)s:%(lineno)d — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(fmt)
        handler.addFilter(TraceContextFilter())
        logging.getLogger(base_logger_name).addHandler(handler)
        return handler

def _detach_file_handler(base_logger_name: str, handler: logging.Handler) -> None:
    with _handler_lock:
        logger = logging.getLogger(base_logger_name)
        try:
            logger.removeHandler(handler)
        finally:
            try:
                handler.close()
            except Exception:
                pass

# -------- Public API --------
def get_logger(name: Optional[str] = None) -> logging.Logger:
    base = logging.getLogger("app")
    return base.getChild(name) if name else base

def start_scope(
    scope_type: Literal["request", "function", "task"],
    base_dir: Path,
    label: str,
    base_logger_name: str = "app",
    reuse_if_exists: bool = True,
) -> ScopeInfo:
    existing = trace_id_var.get()
    stack = list(_scope_stack_var.get())

    if existing and reuse_if_exists:
        # nested scope: reuse handler, push type, no ownership
        stack.append(scope_type)
        _scope_stack_var.set(stack)
        handler_owner_var.set(False)
        handler = current_handler_var.get()
        logfile = Path(getattr(handler, "_scoped_logfile", base_dir / "unknown.log")) if handler else base_dir / "unknown.log"
        return ScopeInfo(existing, scope_type, logfile)

    # new outer scope (or forced new)
    tid = existing or uuid.uuid4().hex
    trace_id_var.set(tid)

    if not existing:
        stack = []
    stack.append(scope_type)
    _scope_stack_var.set(stack)
    handler_owner_var.set(True)

    day = datetime.now().strftime("%Y-%m-%d")
    subdir = {"request": "requests", "function": "functions", "task": "tasks"}[scope_type]
    dirpath = base_dir / subdir / day
    ensure_dir(dirpath)
    logfile = dirpath / f"{now_ms_str()}__{safe_filename(label)}__{tid}.log"

    handler = _attach_file_handler(base_logger_name, logfile)
    setattr(handler, "_scoped_logfile", logfile)
    current_handler_var.set(handler)
    return ScopeInfo(tid, scope_type, logfile)

def end_scope(base_logger_name: str = "app") -> Optional[Path]:
    stack = list(_scope_stack_var.get())
    if stack:
        stack.pop()
        _scope_stack_var.set(stack)

    handler = current_handler_var.get()
    logfile = Path(getattr(handler, "_scoped_logfile", "")) if handler else None
    owner = handler_owner_var.get()

    if owner and handler:
        _detach_file_handler(base_logger_name, handler)
        current_handler_var.set(None)
        handler_owner_var.set(False)
        trace_id_var.set(None)
        _scope_stack_var.set([])

    return logfile
