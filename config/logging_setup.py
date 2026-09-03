import logging
import os
import sys
from pathlib import Path

DEFAULT_LOG_DIR = Path("logs")
DEFAULT_LOG_FILE = DEFAULT_LOG_DIR / "auto-bid.log"


def setup_logging(
    level: str | None = None,
    log_file: Path | None = None,
) -> Path:
    """Configure root logger with console and file output. Returns the log file path."""
    log_level = (level or os.environ.get("LOG_LEVEL", "INFO")).upper()
    log_path = log_file or Path(os.environ.get("LOG_FILE", str(DEFAULT_LOG_FILE)))

    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(log_level)
    root.handlers.clear()

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root.addHandler(console)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    return log_path
