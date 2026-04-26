import os

_settings = None


class Configuration:
    def __init__(self):
        self.JWT_SECRET = os.getenv("JWT_SECRET")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
        self.MONGODB_URL = os.getenv("MONGODB_URL")
        self.DB_NAME = os.getenv("DB_NAME")
        self.OCR_URL = os.getenv("OCR_URL")

        self._validate()

    def _validate(self):
        if not self.JWT_SECRET:
            raise ValueError("'JWT_SECRET' is not set!")

        valid_algos = ["HS256", "HS512"]
        if self.JWT_ALGORITHM not in valid_algos:
            raise ValueError(
                f"Unspported algorithm: {self.JWT_ALGORITHM}. Choose from supported algorithms: {valid_algos}"
            )

        valid_log_levels = ["INFO", "DEBUG"]
        if self.LOG_LEVEL not in valid_log_levels:
            raise ValueError(
                f"Invalid log level: {self.LOG_LEVEL}. Available log levels: {valid_log_levels}"
            )

        if not self.MONGODB_URL:
            raise ValueError("'MONGODB_URL' is not set!")

        if not self.DB_NAME:
            raise ValueError("'DB_NAME' is not set!")

        if not self.OCR_URL:
            raise ValueError("'OCR_URL' is not set!")


def init_config():
    global _settings
    if _settings is None:
        _settings = Configuration()
    return _settings


def get_configuration():
    if _settings is None:
        raise RuntimeError("Configuration is not initialized!")
    return _settings
