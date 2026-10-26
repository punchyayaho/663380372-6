# src/utils.py
import datetime
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_logging(name, level=logging.INFO):
    """Sets up a logger for a module (one handler, no duplicate lines)."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(ch)
        logger.propagate = False
    return logger


def ensure_directory_exists(path):
    """Ensures that a directory exists, creating it if necessary."""
    if path:
        os.makedirs(path, exist_ok=True)


def log_audit_entry(audit_log, status, message, task_type="N/A", details=None):
    """Appends an entry to the in-memory audit log."""
    audit_log.append({
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "task_type": task_type,
        "message": message,
        "details": details or {},
    })


def save_audit_report(audit_log, directory):
    """Saves the audit log as a JSON file and returns its path."""
    ensure_directory_exists(directory)
    path = os.path.join(directory, f"audit_report_{datetime.datetime.now():%Y%m%d_%H%M%S}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(audit_log, f, indent=2, ensure_ascii=False)
    return path
