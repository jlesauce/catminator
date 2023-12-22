import io
from unittest.mock import Mock

import numpy as np
from PIL import Image

from data.data_file import DataFile


class CatPhoto:
    def __init__(self, rgb_array):
        self.array = rgb_array


class PiCamera(Mock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolution = (640, 480)
        self.rotation = 0
        self.framerate = 30
        self.hflip = False
        self.vflip = False

    @staticmethod
    def capture_continuous(*args, **kwargs):
        def cat_photo_generator(image_path):
            while True:
                image = Image.open(image_path)
                rgb_array = np.array(image)
                cat_photo = CatPhoto(rgb_array)

                yield cat_photo

        return cat_photo_generator(image_path=DataFile("poor_cat.jpg").path)
