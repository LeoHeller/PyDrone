
import sys
sys.path.insert(0, '/home/leo/Desktop/PyDrone/modules/')

import time
import os
from signals import Signals, Bcolors
import utils
import Sockets
import signals
import flight_maneuvers

utils.update = 'Wed Dec 19 09:00:42 2018'
utils.head()


pwd = "admin"
global running
running = True


def _on_message(data):
    '''parse the incoming message

    Arguments:
        data {bytes} -- the incoming message in byte form

    Returns:
        string/bytes -- if a answer is needed it is simply returned
    '''

    global running

    # server quit
    if data == Signals.QUIT or data == b'':
        Sockets.no_connection = True

    # unexpected
    else:
        print(Bcolors.WARNING + "\runexpected data: {}".format(data) + Bcolors.ENDC, end="\n-> ")


def on_message(data):
    # server quit
    if data == Signals.QUIT or data == b'':
        Sockets.no_connection = True
        flight_maneuvers.land()
    else:
        signals.Recive.handle_input(data)


# create the Server object and start it
Server = Sockets.HandleSockets(
    "127.0.0.1", 1337, "admin", mode="s", on_message=on_message)
Server.isDaemon = True
Server.start()

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
