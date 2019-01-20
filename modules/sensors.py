import sys
sys.path.insert(0, '../modules/')  # noqa
import threading
import random
import time
import MPU9250


class Sensors(threading.Thread):
    def __init__(self, send):
        self.send = send
        self.mpu9250 = MPU9250.MPU9250()

        threading.Thread.__init__(self)

    def run(self):
        while True:
            accel = self.mpu9250.readAccel()
            gyro = self.mpu9250.readGyro()
            mag = self.mpu9250.readMagnet()

            self.send(accel["x"], accel["y"], accel["z"], gyro["x"], gyro["y"], gyro["z"], mag["x"], mag["y"], mag["z"])

            time.sleep(0.5)
