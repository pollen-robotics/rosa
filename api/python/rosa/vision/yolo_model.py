import cv2 as cv
import numpy as np

from PIL import Image
from keras.utils import get_file

from .yolov3 import YoloV3

PRETRAINED_WEIGHTS = {
    'name': 'rosa-yolo-res256x320.h5',
    'origin': 'https://github.com/pollen-robotics/rosa/releases/download/0.1/rosa-yolo-res256x320.h5',
    'hash': 'fa9a254e4c00420430dd13d5a2eedda4068d71e6f44be475fa20120e6c62c90e',
}


class YoloModel(object):
    _model = None

    @classmethod
    def detect_objects(cls, img):
        if YoloModel._model is None:
            cls.load_model()

        img = cv.resize(img, (640, 480))
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)

        pil_img, res = YoloModel._model.detect_image(pil_img)

        img = np.asarray(pil_img)
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

        return img, res

    @classmethod
    def get_class_name(cls, i):
        if YoloModel._model is None:
            cls.load_model()
        return YoloModel._model.class_names[i]


    @classmethod
    def load_model(cls):
        model_path = get_file(
            fname=PRETRAINED_WEIGHTS['name'],
            origin=PRETRAINED_WEIGHTS['origin'],
            cache_subdir='rosa',
            file_hash=PRETRAINED_WEIGHTS['hash']
        )
        model = YoloV3(
            model_path=model_path,
            anchors_path='./vision/yolo/tiny_yolo_anchors.txt',
            classes_path='./vision/yolo/classes.txt',
            model_image_size=(256, 320),
            score=0.2,
            iou=0.15,
        )

        YoloModel._model = model
