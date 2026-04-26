import os
import logging
from typing import List, Optional

# Belső globális változó a példánynak
_settings: Optional['Configuration'] = None
logger = logging.getLogger(__name__)

class Configuration:
    def __init__(self):
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
        
        raw_langs = os.getenv("OCR_LANGUAGES", "hu,en")
        self.OCR_LANGUAGES: List[str] = [
            l.strip() for l in raw_langs.split(",") if l.strip()
        ]

        gpu_raw = os.getenv("GPU_ENABLED", "false").lower()
        self.GPU_ENABLED: bool = gpu_raw in ("true", "yes")

        self._validate()

    def _validate(self):
        valid_levels = ["INFO", "DEBUG"]
        if self.LOG_LEVEL not in valid_levels:
            raise ValueError(
                f"Invalid log level: {self.LOG_LEVEL}. Available log levels: {valid_log_levels}"
            )

def init_config() -> Configuration:
    global _settings
    if _settings is None:
        _settings = Configuration()
    return _settings

def get_configuration() -> Configuration:
    if _settings is None:
        raise RuntimeError("Configuration is not initilized!")
    return _settings