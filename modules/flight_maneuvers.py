"""functions for in flight maneuvers."""

import sys
import time
import utils
sys.path.insert(0, '/home/leo/Desktop/PyDrone/Droneside/')  # noqa

from motors import Motors


motors = Motors()


motorspeeds = [0, 0, 0, 0]


def set_speed(motorID, speed):
    """Set speed on {motorID0} to {speed}."""
    motors.set_speed(motorID, speed)
    motorspeeds[motorID] = speed


def land():
    """Land the drone."""
    avg_speed = int(sum(motorspeeds)/len(motorspeeds))
    while motorspeeds != [avg_speed, avg_speed, avg_speed, avg_speed]:
        for motor in range(4):
            if motorspeeds[motor] is not avg_speed:
                if motorspeeds[motor] > avg_speed:
                    set_speed(motor, max(motorspeeds[motor]-1, 0))
                    #motorspeeds[motor] -= 1
                else:
                    set_speed(motor, max(motorspeeds[motor]+1, 0))

                time.sleep(0.2)
        print(motorspeeds)


def arm():
    """Arm all escs."""
    for motor in range(4):
        set_speed(motor, 100)
        set_speed(motor, 0)
        time.sleep(1)


def set_all(speed):
    """Set all motors to {speed}."""
    for motor in motors.motors:
        set_speed(motor, speed)
