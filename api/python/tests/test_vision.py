import numpy as np
import unittest

from rosa.vision import detect_objects, get_line_center


class VisionTestCase(unittest.TestCase):
    RES = 320, 256, 3

    def setUp(self):
        self.img = self.generate_random_image()

    def test_line_detector(self):
        center = get_line_center(self.img)
        self.assertIsNone(center)

    def test_obj_detector(self):
        obj = detect_objects(self.img)
        self.assertEqual(len(obj), 0)

    def generate_random_image(self):
        return np.uint8(np.random.rand(*VisionTestCase.RES) * 255)
