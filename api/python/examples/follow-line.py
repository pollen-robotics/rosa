from __future__ import division

import cv2 as cv

from rosa import Rosa
from rosa.vision import get_line_center


def look_around(rosa, speed=0.25):
    rosa.left_wheel.speed = speed
    rosa.right_wheel.speed = -speed


def follow_line(rosa, center, gain=0.4, img_width=320):
    dx, _ = center

    dx = ((dx / img_width) - 0.5) * 2

    ls = gain * (0.5 * -dx + 0.5)
    rs = gain * (0.5 * dx + 0.5)

    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs


if __name__ == '__main__':
    rosa = Rosa('rosa.local')

    while True:
        img = rosa.camera.last_frame
        if img is None:
            continue
        center = get_line_center(img, render=True)

        if center is None:
            look_around(rosa)

        else:
            follow_line(rosa, center)

        cv.imshow('follow line', img)
        cv.waitKey(1)
