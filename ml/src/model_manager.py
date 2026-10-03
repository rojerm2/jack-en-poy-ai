import logging
from pathlib import Path
from threading import RLock

from src.prediction import ModelUnavailable, Predictor

logger = logging.getLogger(__name__)


class ModelManager:
    """Swap only fully validated predictors; requests retain an immutable snapshot."""
    def __init__(self, path):
        self.path = Path(path)
        self.lock = RLock()
        self.predictor = None
        self.signature = object()
        self.reload_failed = False

    def get(self):
        with self.lock:
            try:
                stat = self.path.stat()
                signature = (stat.st_mtime_ns, stat.st_size)
            except OSError:
                signature = None
            if signature != self.signature:
                self.signature = signature
                try:
                    candidate = Predictor(self.path)
                    self.predictor = candidate
                    self.reload_failed = False
                except ModelUnavailable:
                    self.reload_failed = True
                    logger.warning("Model reload failed; retaining the last valid predictor if available.")
            return self.predictor
