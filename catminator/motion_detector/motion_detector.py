import logging
from datetime import datetime
from threading import Thread

import numpy as np

from catminator.camera.camera import Camera
from catminator.notification.Notificator import Notificator

logger = logging.getLogger(__name__)

pixel_motion_threshold = 20
motion_sensitivity_in_pixels = 300


class MotionDetector:
    def __init__(self, camera: Camera):
        self.camera = camera
        self.detection_thread = None
        self.is_detection_thread_stopped = False
        self.last_frame = None
        self.notificator = Notificator()

    def start_detection(self):
        self.detection_thread = Thread(target=self.run, args=())
        self.detection_thread.daemon = True
        self.is_detection_thread_stopped = False

        logger.debug(f'Start motion detector thead')
        self.detection_thread.start()

    def run(self):
        self.camera.start_camera()

        for frame in self.camera.get_stream():
            self.last_frame = frame.array
            self.camera.clear_stream()

            if self.is_detection_thread_stopped:
                self.camera.stop_camera()
                break

        logger.debug("Motion detector thread stopped")

    def stop_detection(self):
        logger.debug(f'Stopping motion detector thead')
        self.is_detection_thread_stopped = True

    def join(self):
        self.detection_thread.join()

    def detect_motion(self, frame1, frame2):
        pixels_changed = (np.absolute(frame1 - frame2) > pixel_motion_threshold).sum() / 3

        if pixels_changed > motion_sensitivity_in_pixels:
            logger.info(f"Motion detected ({pixels_changed=}, "
                        f"{motion_sensitivity_in_pixels=},  {pixel_motion_threshold=})")
            self.notify_motion()

    def notify_motion(self):
        self.notificator.push_note("Motion detected",
                                   f"Motion detected by the camera at {datetime.timestamp(datetime.now())}")
