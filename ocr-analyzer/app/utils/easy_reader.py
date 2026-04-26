import os
import easyocr

from app.utils.config import get_configuration
from app.utils.logger import logger


class OCRReaderSingleton:
    _reader = None

    def __init__(self):
        try:
            conf = get_configuration()
            self._reader = easyocr.Reader(conf.OCR_LANGUAGES, gpu=conf.GPU_ENABLED)

            logger.info(
                "EasyOCR is initilized, GPU_ENBALED=%s, languages=%s",
                str(conf.GPU_ENABLED),
                str(conf.OCR_LANGUAGES),
            )

        except Exception as e:
            logger.error(f"Failed to initilize EasyOCR {e}")
            raise e

    def get_reader(self):
        return self._reader


def get_ocr_reader():
    return OCRReaderSingleton().get_reader()
