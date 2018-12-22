"""functions for in flight maneuvers."""

import sys
import time
sys.path.insert(0, '/home/leo/Desktop/PyDrone/Droneside/')  # noqa

from motors import Motors


motors = Motors()


def set_speed(motorID, speed):
    """Set speed on {motorID0} to {speed}."""
    motors.set_speed(motorID, speed)


def land():
    """Land the drone."""
    for speed in range(50, -1, -1):
        set_all(speed)
        time.sleep(0.2)


def set_all(speed):
    """Set all motors to {speed}."""
    for motor in motors.motors:
        set_speed(motor, speed)
