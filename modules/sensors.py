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
        self.degrees = [0, 0, 0]
        self.last_degrees = self.degrees

        threading.Thread.__init__(self)
        sensor_thread = DoEvery(self.DeltaTime, self.read)

    def integrate(self, l):
        counter = 0
        for axis in l:
            axis *= self.deltaTime
            degrees[counter] += axis
            counter += 1

    def read(self):
        gyro = self.mpu9250.readGyro()
        for i in [0, 1, 2]:
            if abs(gyro[i]) > 0.1:
                pass
            else:
                gyro[i] = 0
        self.integrate(gyro)

    def stop(self):
        self._stop = True

    def run(self):
        while not self._stop:
            if self.degrees != self.last_degrees:
                print(*self.degrees)
                self.send(*self.degrees)
                time.sleep(0.1)
                self.last_degrees = self.degrees
