# Python's API for the ROSA robot

Rosa can be controlled through WiFi via a Python's API. This API lets you control the robot: make it move, read its distance or color sensors and access its camera to retrieve an image. It also provides higher level functionalities like detecting a line or specific objects in an image.

The full API is described below. You can also find various examples illustrating how to use it [here](./examples).

## Getting started

The Python package to control Rosa can be installed via:

```
pip install rosa
```

Or directly from the source of this repository.

It is compatible with Python versions 2.7 or >= 3.4. It uses a websocket library to communicate with the robot and numpy, opencv and keras for the computer vision.

Once installed, you should be able to connect to your robot via the following python code:

```
from rosa import Rosa

rosa = Rosa('rosa.local')
```

*Note: This assumes that your robot is connected to the same WiFi network and accessible via this hostname. See the [main documentation](https://github.com/pollen-robotics/rosa) for details.*

## Navigation

### Motor control

To make your robot move, you can change the speed of its wheels. For the left wheel:

```
rosa.left_wheel.speed = 0.25
```

And for the right wheel:

```
rosa.right_wheel.speed = 0.25
```

The speed is expressed as a ratio of the maximum speed. This means that *0.25* represents 25% of the maximum speed and *1.0* represents the maximum reachable speed.
Positive speed means the robot is moving forward, while negative speeds will make the robot goes backward.

To stop the robot, set its speeds to 0.0:

```
rosa.left_wheel.speed = 0
rosa.right_wheel.speed = 0
```

For a more complete example, you can check:

* [simple demo movements](./examples/move.py)

### Distance sensor

**TODO**

## Vision

The robot is also equipped with a camera. You can access the last image from the camera via:

```
img = rosa.camera.last_frame
```

*Please note that the results could be None if the camera fails to grab an image. In this case simply retries to grab an image slightly later.*

The image is returned as an [OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html) image and can thus be used as such.

The camera resolution is 640x480 by default and you should be able to reach about 20fps depending on your network bandwidth.

### Line detection

This package provides you with a pre-defined line detector that works on the image. You can access it like this (where img is an image):

```
from rosa.vision import get_line_center

line_center = get_line_center(rosa.camera.last_frame)
x, y = line_center
```

The found center is expressed in pixels coordinates from the image.

You can also ask to draw the found center on the image and display it using OpenCV like this for instance:

```
import cv2 as cv

img = rosa.camera.last_frame
line_center = get_line_center(img, render=True)

cv.imshow('line-detector', img)
cv.waitKey(-1)
```

For a more complete example, you can check:

* [a follow line behavior](./examples/follow-line.py) where the robot will turn on itself until it finds a black line and then follow it

### Object detection

You also have accessed to object detection using a pre-trained neural network (based on the YOLOv3 algorithm).It can be directly used like this:

```
from rosa.vision import detect_objects

found_objects = detect_objects(rosa.camera.last_frame)
```

The return *found_objects* will contain a list of all the objects detected in the image. For each object, you will have access to:

* a **label** (among *ball*, *cube* or *star*)
* the **center** of the object (expressed in pixel coordinates)
* a quadruplet for the **bounding_box** of the object: (x_min, y_min, x_max, y_max) also expressed in pixel coordinates
* a **confidence** score on the result

You can access those informations like this:

```
for obj in found_objects:
    print('Found: ', obj.label, 'at: ', obj.center)
```

You can also directly render the detection on the image via:

```
import cv2 as cv

img = rosa.camera.last_frame
found_objects = detect_objects(img, render=True)

cv.imshow('object-detector', img)
cv.waitKey(-1)
```

For more complete examples, you can check:

* [a visualisation example for object detection](./examples/obj-detection-visu.py)
* [a tiny game](./examples/get-cube-and-freeze.py) where the robot will turn around itself until it finds a cube and grabs it. It will then freeze until you remove its cube and then it will look again.
