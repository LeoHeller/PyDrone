import sys
sys.path.insert(0, '/home/leo/Desktop/PyDrone/Droneside/')

from motors import Motors
import time


motors = Motors()


def set_speed(motorID, speed):
    motors.set_speed(motorID, speed)


def land():
    for speed in range(50, -1, -1):
        set_all(speed)
        time.sleep(0.2)


def set_all(speed):
    for motor in motors.motors:
        set_speed(motor, speed)
