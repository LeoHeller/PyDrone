import ctypes
import sys

import math

sys.path.insert(0, '../modules/')  # noqa
from ctypes import cdll

import MPU9250

import numpy as np

lib = cdll.LoadLibrary('../modules/libmad.so')
lib.get_q0.restype = ctypes.c_float
lib.get_q1.restype = ctypes.c_float
lib.get_q2.restype = ctypes.c_float
lib.get_q3.restype = ctypes.c_float
py_update_imu = lib.MadgwickAHRSupdateIMU
py_update_imu.argtypes = [ctypes.c_float, ctypes.c_float,
                          ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
py_update_9dof = lib.MadgwickAHRSupdate
py_update_9dof.argtypes = [ctypes.c_float] * 9

set_beta = lib.set_beda
set_beta.argtypes = [ctypes.c_float]


class Sensors:
    def __init__(self):
        set_beta(0.1)
        self.mpu9250 = MPU9250.MPU9250()
        # self.DeltaTime = 0.02
        # self._stop = False
        self.raw_integrated_gyro = [0, 0, 0]
        self.degrees = [0, 0, 0]
        self.mag_yaw = 0
        self.last_correct_roll = 0
        self.last_correct_pitch = 0
        self.correct_roll = 0
        self.correct_pitch = 0

        # sensor_thread = DoEvery(self.DeltaTime, self.read)
        # sensor_thread.start()

    def read(self):

        gyro = self.mpu9250.readGyro()
        gyro = np.multiply(gyro, 0.0174533)
        if abs(gyro[0]) < 0.2:
            gyro[0] = 0
        if abs(gyro[1]) < 0.2:
            gyro[1] = 0
        if abs(gyro[2]) < 0.2:
            gyro[2] = 0

        acceleration = self.mpu9250.readAccel()
        mag = self.mpu9250.readMagnet()
        self.mag_yaw = math.atan2(mag[1], mag[0])

        py_update_imu(gyro[0], gyro[1], gyro[2], acceleration[0], acceleration[1], acceleration[2])
        self.degrees = self.to_euler_angles(
            lib.get_q0(), lib.get_q1(), lib.get_q2(), lib.get_q3())
        return self.degrees

    @staticmethod
    def to_euler_angles(q0, q1, q2, q3):
        pitch = np.arcsin(2 * q1 * q2 + 2 * q0 * q3)
        if np.abs(q1 * q2 + q3 * q0 - 0.5) < 1e-8:
            roll = 0
            yaw = 2 * np.arctan2(q1, q0)
        elif np.abs(q1 * q2 + q3 * q0 + 0.5) < 1e-8:
            roll = -2 * np.arctan2(q1, q0)
            yaw = 0
        else:
            roll = np.arctan2(2 * q0 * q1 - 2 * q2 * q3,
                              1 - 2 * q1 ** 2 - 2 * q3 ** 2)
            yaw = np.arctan2(2 * q0 * q2 - 2 * q1 * q3,
                             1 - 2 * q2 ** 2 - 2 * q3 ** 2)
        roll, pitch, yaw = np.multiply([roll, pitch, yaw], 57.2958)
        if roll < 0:
            roll += 2 * 3.141592
        return [roll - 1, pitch, yaw]
