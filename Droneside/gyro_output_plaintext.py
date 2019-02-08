import sys
sys.path.insert(0, '../modules/')  # noqa
import MPU9250
import time
import threading



import timeit
mpu9250 = MPU9250.MPU9250()

def f():
    gyro = mpu9250.readGyro()

f()
print(timeit.timeit(f), setup="import MPU9250")
quit()

i=0
N = 1000
start = time.time()
while i < N:
    #accel = mpu9250.readAccel()
    gyro = mpu9250.readGyro()
    #mag = mpu9250.readMagnet()
    #a_t = "{:=7.3f} {:=7.3f} {:=7.3f}".format(accel["x"], accel["y"], accel["z"])
    #g_t = "{:=7.3f} {:=7.3f} {:=7.3f}".format(gyro["x"], gyro["y"], gyro["z"])
    #m_t = "{:=7.3f} {:=7.3f} {:=7.3f}".format(mag["x"], mag["y"], mag["z"])
    #text = "\raccel: {}, gyro: {}, mag: {}".format(a_t, g_t, m_t)
    #print(text, end="")
    i += 1
print((time.time()-start)/N)
