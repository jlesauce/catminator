from unittest.mock import Mock

from catminator.util.stubs.pi_camera import PiCamera


class PiRGBArray(Mock):
    def __init__(self, pi_camera: PiCamera, size: int = 0):
        super().__init__()
        self.camera = pi_camera
        self.size = size

    def truncate(self):
        pass

    def seek(self, position):
        pass
