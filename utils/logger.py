import os
import time
import threading
from enum import Enum

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3

class AttackLogger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, path="logs"):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.path = path
            self._buffer = []
            self._level = LogLevel.DEBUG
            self._log_count = 0
            os.makedirs(path, exist_ok=True)
            self._session = f"session_{int(time.time())}"

    def log(self, message, level=LogLevel.INFO):
        if level.value < self._level.value:
            return
        ts = time.strftime("%H:%M:%S")
        entry = f"[{ts}][{level.name}] {message}"
        self._buffer.append(entry)
        self._log_count += 1
        if len(self._buffer) >= 100:
            self.flush()

    def flush(self):
        if not self._buffer:
            return
        fname = os.path.join(self.path, f"{self._session}.log")
        with open(fname, "a") as f:
            for entry in self._buffer:
                f.write(entry + "\n")
        self._buffer.clear()

    def stats(self):
        return self._log_count
