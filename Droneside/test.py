import time as t
print("test", end = "")
for i in range(5):
    print("{}\r".format(i), end = "")
    t.sleep(0.2)