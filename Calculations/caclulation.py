"""calculations for drone stats."""

sensors = 0
esc = 4 * 10
props = 8
motors = 4 * 50
frame = 295
battery = 895

weight = sensors + esc + props + motors + frame + battery


batterie_amps = 17.4
draw = 10.6 * 4

thrust = 4 * 710

twratio = thrust / weight

flight_time = batterie_amps / draw * 60


hover_time = flight_time * twratio

print("The Drone will fly for {:.2f}min at full power or hover for {:.2f}min \
using a total of {:.2f}mah \
with a thrust to weight ratio of {:.2f} \
and the quad weighs {:.2f}g".format(flight_time, hover_time, batterie_amps, twratio, weight))
