import time
import numpy as np

from rosa import Rosa


"""
    Exploration mode.

    The robot will goes straightforward until it sees an obstacle or detect void below it.
    It will then do a random turn and keep going.

    The program runs forever until stops via Ctrl-c.
"""


cruise_speed = 0.15

if __name__ == '__main__':
    rosa = Rosa('rosa.local')

    while True:
        dist = np.array([rosa.get_distance(s) for s in rosa.front_distance_sensors])
        obstacle_detected = np.any(dist > 200)

        ground = np.array([rosa.get_distance(s) for s in rosa.ground_distance_sensors])
        void_detected = np.any(ground < 100)

        if obstacle_detected or void_detected:
            rosa.left_wheel.speed = np.random.rand() - 0.5  # random value within [-1/2, 1/2]
            rosa.right_wheel.speed = np.random.rand() - 0.5  # random value within [-1/2, 1/2]

            time.sleep(1)

        rosa.left_wheel.speed = rosa.right_wheel.speed = cruise_speed
        time.sleep(0.1)
