import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np


sensors = 70
esc = 4 * 10
props = 8
motors = 4 * 50
frame = 295
battery = 1000

weight = sensors + esc + props + motors + frame + battery


batterie_amps = 14.790
draw = 10.6 * 4

thrust = 4 * 710

twratio = thrust/weight

flight_time = batterie_amps / draw * 60


hover_time = flight_time * twratio

print("The Drone will fly for {:.2f}min at full power or hover for {:.2f}min using a total of {:.2f}mah with a thrust to weight ratio of {:.2f} and the quad weighs {:.2f}g".format(flight_time, hover_time, batterie_amps, twratio, weight))


objects = ('flight time', 'hover time', 'powerusage', 'Thrust to weight ratio', 'weight')
y_pos = np.arange(len(objects))

performance = [flight_time, hover_time, batterie_amps, twratio, weight]
 
plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Stats')
plt.title('Drone Stats')
 
plt.show()

class Drone():
    def __init__(self, batteries):
        pass
        



    def calculate(self):
        plt.plot([1,2,3,4], [1,4,9,16], 'r-')
        plt.axis([0, 6, 0, 20])
        plt.show()

    def visualize():
        pass



# drone = Drone(1)

# 3000 = 14.8
# 3000/14.8 = 1
# 3000/14.8*11.1

