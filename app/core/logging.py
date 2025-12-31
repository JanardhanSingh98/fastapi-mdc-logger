import logging
import sys
from logging.handlers import RotatingFileHandler

from app.core.settings import get_settings
from app.utils.mdc import get_mdc

_old_factory = logging.getLogRecordFactory()
settings = get_settings()


def record_factory(*args, **kwargs):
    record = _old_factory(*args, **kwargs)

    mdc = get_mdc()
    request_id = mdc.get("request_id")
    user_id = mdc.get("user_id")

    parts = []
    if request_id:
        parts.append(f"request_id={request_id}")
    if user_id:
        parts.append(f"user_id={user_id}")

    if parts:
        record.msg = f"[{' '.join(parts)}] {record.msg}"

    return record


def setup_logging():
    logging.setLogRecordFactory(record_factory)

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    # ---- File handler ----
    file_handler = RotatingFileHandler(filename="logs/app.log", maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)

    # ---- Console handler ----
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Avoid duplicate handlers on reload
    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
