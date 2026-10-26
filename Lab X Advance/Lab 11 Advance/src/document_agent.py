# src/document_agent.py
import datetime
import os

from .pdf_tasks import PDFTasks
from .word_tasks import WordTasks
from .utils import setup_logging, log_audit_entry, save_audit_report

logger = setup_logging(__name__)


class DocumentAgent:
    """
    Config-driven agent: reads a list of tasks and executes them in order
    (merge PDFs, generate Word report from template, watermark PDF),
    recording every step in an audit log.
    """

    def __init__(self, config, base_dir):
        self.config = config
        self.base_dir = base_dir
        self.pdf = PDFTasks()
        self.word = WordTasks()
        self.audit_log = []
        self.results = {"success": 0, "failed": 0}

    def _path(self, relative):
        return os.path.join(self.base_dir, relative)

    def _run_task(self, number, task):
        task_type = task["type"]
        name = task.get("name", task_type)
        logger.info(f"--- Task {number}: {name} ({task_type}) ---")
        try:
            if task_type == "merge_pdfs":
                pages = self.pdf.merge_pdfs([self._path(p) for p in task["input_files"]], self._path(task["output_file"]))
                detail = {"output": task["output_file"], "pages": pages}
            elif task_type == "generate_report":
                filled = self.word.generate_report(self._path(task["template"]), self._path(task["output_file"]),
                                                   task["context"], task.get("table"))
                detail = {"output": task["output_file"], "placeholders_filled": filled}
            elif task_type == "add_watermark":
                pages = self.pdf.add_watermark(self._path(task["input_file"]), self._path(task["output_file"]),
                                               task["watermark_text"], task.get("opacity", 0.25),
                                               task.get("font_size", 72), task.get("angle", 45))
                detail = {"output": task["output_file"], "pages": pages}
            else:
                raise ValueError(f"Unsupported task type: {task_type}")
            self.results["success"] += 1
            log_audit_entry(self.audit_log, "SUCCESS", f"Task '{name}' completed.", task_type, detail)
        except Exception as e:
            self.results["failed"] += 1
            logger.error(f"Task '{name}' failed: {e}")
            log_audit_entry(self.audit_log, "ERROR", f"Task '{name}' failed: {e}", task_type)

    def run(self):
        start = datetime.datetime.now()
        logger.info(f"Document Agent started with {len(self.config['tasks'])} task(s).")
        for i, task in enumerate(self.config["tasks"], start=1):
            self._run_task(i, task)
        seconds = (datetime.datetime.now() - start).total_seconds()
        log_audit_entry(self.audit_log, "INFO", f"Agent finished in {seconds:.2f}s", "run_summary", self.results)
        report = save_audit_report(self.audit_log, self._path("reports"))
        logger.info(f"Audit report saved: {report}")
        logger.info(f"Summary: {self.results['success']} succeeded, {self.results['failed']} failed.")
        return self.results
