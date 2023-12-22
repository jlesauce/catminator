import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigFile:

    def __init__(self, file_name: str):
        self.path = Path(__file__).parent / file_name
        if not self.path.exists():
            raise FileNotFoundError(f'File {self.path} does not exist')

    def load(self):
        import yaml
        with open(self.path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.error(f"Failed to load config file {self.path}: {exc}")

    def __str__(self):
        return str(self.path)
