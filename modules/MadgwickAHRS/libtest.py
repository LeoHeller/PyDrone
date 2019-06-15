from ctypes import *
import os

cwd = os.getcwd()
lib = cdll.LoadLibrary(cwd+"/libmad.so")
lib.get_q0.restype = c_float
print(lib.get_q0())
