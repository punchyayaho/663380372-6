# main.py
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.config_parser import ConfigParser
from src.document_agent import DocumentAgent
from src.utils import setup_logging

logger = setup_logging(__name__)


def main():
    config_path = os.path.join(BASE_DIR, "configs", "document_tasks_config.json")
    try:
        config = ConfigParser(config_path).load_config()
        agent = DocumentAgent(config, BASE_DIR)
        results = agent.run()
        if results["failed"] == 0:
            logger.info("All document tasks completed. Outputs are in documents/output/")
        else:
            logger.warning("Some tasks failed - check the log above and reports/audit_report_*.json")
    except FileNotFoundError as e:
        logger.critical(f"File not found: {e}. Run 'python create_sample_documents.py' first.")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}")


if __name__ == "__main__":
    main()
