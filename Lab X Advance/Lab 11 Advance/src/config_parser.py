# src/config_parser.py
import json
import os
from .utils import setup_logging

logger = setup_logging(__name__)

# Required parameters for each supported task type
REQUIRED_FIELDS = {
    "merge_pdfs": ["input_files", "output_file"],
    "generate_report": ["template", "output_file", "context"],
    "add_watermark": ["input_file", "output_file", "watermark_text"],
}


class ConfigParser:
    """Loads and validates the document automation configuration (JSON)."""

    def __init__(self, config_path):
        self.config_path = config_path

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in config file: {e}")
        self._validate(config)
        logger.info(f"Configuration loaded and validated: {self.config_path}")
        return config

    def _validate(self, config):
        if not isinstance(config.get("tasks"), list):
            raise ValueError("Config must contain a 'tasks' list.")
        for i, task in enumerate(config["tasks"]):
            task_type = task.get("type")
            if task_type not in REQUIRED_FIELDS:
                raise ValueError(f"Task {i} has unsupported or missing 'type': {task_type}")
            for field in REQUIRED_FIELDS[task_type]:
                if field not in task:
                    raise ValueError(f"Task {i} ({task_type}) is missing required field '{field}'.")
