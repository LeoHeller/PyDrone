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
            gyro = self.mpu9250.readGyro()
            for i in [0,1,2]:
                if abs(gyro[i]) > 0.15:
                    pass
                else:
                    gyro[i] = 0
            self.send(*gyro)
            time.sleep(0.2)
