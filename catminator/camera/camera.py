import logging

from catminator.camera.camera_config import CameraConfig

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    logging.getLogger(__name__).warning("Picamera not found, using mock instead")
    from catminator.util.stubs.pi_camera import PiCamera
    from catminator.util.stubs.pi_rgb_array import PiRGBArray

logger = logging.getLogger(__name__)


class Camera:
    def __init__(self, camera_config: CameraConfig = CameraConfig()):
        self.camera_config = camera_config
        self.camera = None
        self.raw_capture_buffer = None
        self.camera_stream = None

    def start_camera(self):
        logger.debug("Starting camera")
        self.camera = PiCamera()
        self._initialize_camera_config()
        self.raw_capture_buffer = PiRGBArray(self.camera, size=self.camera_config.resolution)
        self.camera_stream = self.camera.capture_continuous(self.raw_capture_buffer, format="rgb", use_video_port=True)

    def stop_camera(self):
        logger.debug("Stopping camera")
        self.camera_stream.close()
        self.raw_capture_buffer.close()
        self.camera.close()

    def get_stream(self):
        return self.camera_stream

    def clear_stream(self):
        self.raw_capture_buffer.truncate()
        self.raw_capture_buffer.seek(0)

    def _initialize_camera_config(self):
        self.camera.resolution = self.camera_config.resolution
        self.camera.rotation = self.camera_config.rotation
        self.camera.framerate = self.camera_config.frame_rate
        self.camera.hflip = self.camera_config.horizontal_flip
        self.camera.vflip = self.camera_config.vertical_flip
