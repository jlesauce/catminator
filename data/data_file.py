import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class DataFile:

    def __init__(self, file_name: str):
        self.path = Path(__file__).parent / file_name
        if not self.path.exists():
            raise FileNotFoundError(f'File {self.path} does not exist')

    def __str__(self):
        return str(self.path)
