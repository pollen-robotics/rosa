import cv2 as cv
import numpy as np

from PIL import Image

from vision.yolo import YOLO
from remote_capture import RemoteCapture
from remote_controller import RemoteController
from follow_utils import look_and_follow


if __name__ == '__main__':
    cap = RemoteCapture('ws://rosa.local:5678')

    controller = RemoteController('ws://rosa.local:1234')
    controller.setup(
        AIN1=18, AIN2=17, PWMA=4,
        BIN1=24, BIN2=27, PWMB=22,
        STBY=23
    )

    yolo = YOLO(
        model_path='./vision/yolo_trained.h5',
        anchors_path='./vision/yolo/tiny_yolo_anchors.txt',
        classes_path='./vision/yolo/classes.txt',
        model_image_size=(256, 320),
        score=0.2,
        iou=0.15,
    )

    while True:
        b, img = cap.read()
        if not b:
            continue

        img = cv.resize(img, (640, 480))
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        pil_img = Image.fromarray(img)
        pil_img, res = yolo.detect_image(pil_img)
        boxes, scores, classes = res

        classes = np.array([yolo.class_names[c] for c in classes])
        cubes = np.array([i for i, c in enumerate(classes)
                         if c == 'cube'], dtype='int64')
        cubes_box = boxes[cubes]
        cubes_center = [
            ((lx + 0.5 * (rx - lx)), (ly + 0.5 * (ry - ly)))
            for (ly, lx, ry, rx) in cubes_box
        ]
        width, height = pil_img.size
        cubes_center = [
            (((x / width) * 2 - 1), -((y / height) * 2 - 1))
            for (x, y) in cubes_center
        ]
        gathered_cubes = [c for c in cubes_center if c[1] < -0.65]
        cubes_to_gather = [c for c in cubes_center if c[1] > -0.65]

        if len(gathered_cubes):  # We got a cube, so we stop!
            controller.set_speed('a', 0)
            controller.set_speed('b', 0)
        else:
            target = cubes_to_gather[0] if len(cubes_to_gather) >= 1 else None
            look_and_follow(controller, target, look_speed=0.15, asserv_p=0.4)

        res = np.asarray(pil_img)
        res = cv.cvtColor(res, cv.COLOR_RGB2BGR)
        cv.imshow('Get Cube', res)
        cv.waitKey(1)
