import sys
sys.path.insert(0, '../modules/')  # noqa
import threading
import random
import time
import MPU9250


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
        accel = self.mpu9250.readAccel()

        for i in [0, 1, 2]:
            if abs(gyro[i]) > 0.2:
                pass
            else:
                gyro[i] = 0
        self.integrate(gyro)
        self.degrees = self.filter_complementary(self.raw_integrated_gyro, accel)

    def filter_complementary(self, integrated_gyro, accelerometer, ratio=0.98):
        filtered = []
        for index in [0,1,2]:
            filtered.append(round(integrated_gyro[index] * (1-ratio) + accelerometer[index] * ratio),1)
        return filtered


    def stop(self):
        self._stop = True

    def run(self):
        while not self._stop:
            # if self.degrees != self.last_degrees:
            # print(*self.degrees)
            self.send(*self.degrees)
            time.sleep(0.1)
            #    self.last_degrees = self.degrees
