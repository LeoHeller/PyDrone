"""Server that runs on the drone."""
import os
import sys
import time
sys.path.insert(0, '../modules/')  # noqa

from PID import PID

import Sockets

import flight_maneuvers

import sensors

import signals
from signals import Bcolors, Signals


pwd = "admin"
global running
running = True


def on_message(data):
    """Quit if the other side quit, otherwise have the input handled."""
    # other side quit
    if data == Signals.QUIT or data == b'':
        Sockets.no_connection = True
        flight_maneuvers.land()
    elif data == Signals.ARM:
        flight_maneuvers.arm()
    else:
        signals.Recive.handle_input(data)

def send_telemetry(x,y,z):
    """function for sending the telemetry data to UI

    Arguments:
        agrs {float} -- value of arg
    """

    Server.send(signals.Send.telemetry(x,y,z))



# create the Server object and start it
Server = Sockets.HandleSockets(
    "192.168.10.1", 1337, "admin", mode="s", on_message=on_message)
Server.isDaemon = True
Server.start()



# create sensor thread
Sensors = sensors.Sensors(send=send_telemetry)
Sensors.isDaemon = True
Sensors.start()








# get user input
try:
    while running:
        i = input("\r-> ")
        # parse for commands
        if i == "q":
            Server.close_all()
            Sockets.should_be_running = False
            exit()
            Server.join()
            print("server joined")
            running = False
            # os._exit(1)
        elif i == "b":  # benchmark
            Server.send(Signals.TIME)
            print(time.time())
        elif i == "crash":
            os._exit(1)
        # send if no command is recognized
        elif not Sockets.no_connection:
            Server.send(i)

except Exception:
    Server.close_all()
    os._exit(1)

Server.close_all()
os._exit(1)
