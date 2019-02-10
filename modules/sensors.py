import sys
sys.path.insert(0, '../modules/')  # noqa
import threading
import random
import time
import MPU9250
import numpy as np

from ctypes import cdll
import ctypes

lib = cdll.LoadLibrary('../modules/libmad.so')
lib.get_q0.restype = ctypes.c_float
lib.get_q1.restype = ctypes.c_float
lib.get_q2.restype = ctypes.c_float
lib.get_q3.restype = ctypes.c_float
py_update = lib.MadgwickAHRSupdateIMU
py_update.argtypes = [ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float, ctypes.c_float]
set_beta = lib.set_beda
set_beta.argtypes = [ctypes.c_float]



class DoEvery(threading.Thread):
    def __init__(self, period, f):
        super().__init__()
        self.period = period
        self.f = f
        self.daemon = True
        self._stop = False

    def stop(self):
        self._stop = True

    def g_tick(self):
        t = time.time()
        count = 0
        while True:
            count += 1
            yield max(t+count*self.period - time.time(), 0)

    def run(self):
        g = self.g_tick()
        while not self._stop:
            time.sleep(next(g))
            self.f()


class Sensors(threading.Thread):
    def __init__(self, send):
        set_beta(10)
        self.send = send
        self.mpu9250 = MPU9250.MPU9250()
        self.DeltaTime = 0.05
        self._stop = False
        self.raw_integrated_gyro = [0, 0, 0]
        self.degrees = [0, 0, 0]
        self.last_degrees = self.degrees

        threading.Thread.__init__(self)
        sensor_thread = DoEvery(self.DeltaTime, self.read)
        sensor_thread.start()

    def integrate(self, l):
        counter = 0
        for axis in l:
            axis *= self.DeltaTime
            self.raw_integrated_gyro[counter] += axis
            counter += 1

    def read(self):
        gyro = self.mpu9250.readGyro()
        gyro = np.multiply(gyro, 0.0174533)
        accel = self.mpu9250.readAccel()

        # for i in [0, 1, 2]:
        #     if abs(gyro[i]) > 0.2:
        #         pass
        #     else:
        #         gyro[i] = 0
        py_update(gyro[0], gyro[1], gyro[2], accel[0], accel[1], accel[2])


    def to_euler_angles(self, q0,q1,q2,q3):
        pitch = np.arcsin(2 * q1 * q2 + 2 * q0 * q3)
        if np.abs(q1 * q2 + q3 * q0 - 0.5) < 1e-8:
            roll = 0
            yaw = 2 * np.arctan2(q1, q0)
        elif np.abs(q1 * q2 + q3 * q0 + 0.5) < 1e-8:
            roll = -2 * np.arctan2(q1, q0)
            yaw = 0
        else:
            roll = np.arctan2(2 * q0 * q1 - 2 * q2 * q3, 1 - 2 * q1 ** 2 - 2 * q3 ** 2)
            yaw = np.arctan2(2 * q0 * q2 - 2 * q1 * q3, 1 - 2 * q2 ** 2 - 2 * q3 ** 2)
        return np.multiply([roll, pitch, yaw],57.2958)

    def stop(self):
        self._stop = True

    def run(self):
        while not self._stop:
            # if self.degrees != self.last_degrees:
            # print(*self.degrees)

            self.send(*self.to_euler_angles(lib.get_q0(), lib.get_q1(), lib.get_q2(), lib.get_q3()))
            time.sleep(0.1)
            #    self.last_degrees = self.degrees
