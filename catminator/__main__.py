import argparse
import logging
import os

from catminator.camera.camera import Camera
from catminator.motion_detector.motion_detector import MotionDetector
from catminator.util.logger import configure_logger

APPLICATION_NAME = "Cat Detector"

logger = logging.getLogger(__name__)
motion_detector = MotionDetector(camera=Camera())


def main():
    args = _parse_arguments()
    configure_logger(log_level=logging.getLevelName(args.log_level.upper()))

    logger.info(f'Start {APPLICATION_NAME}')
    motion_detector.start_detection()
    motion_detector.join()


def _parse_arguments():
    parser = _create_argument_parser()
    return parser.parse_args()


def _create_argument_parser():
    parser = argparse.ArgumentParser(
        description='Application used to detect cats in images.')
    parser.add_argument('--log-level', dest="log_level",
                        choices=['debug', 'info', 'warn', 'error', 'fatal'], default='debug',
                        help="Set the application log level")
    return parser


def _is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    return arg


if __name__ == "__main__":
    main()
