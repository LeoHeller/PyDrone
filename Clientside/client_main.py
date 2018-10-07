import os
import sys
import time

sys.path.insert(0, '/home/leo/Desktop/PyDrone/modules/')

import Sockets
import utils
from signals import Bcolors, Signals




utils.update = "Sun Oct  7 11:27:34 2018"
utils.head()


pwd = "admin"
running = True

def on_message(data):
    '''parse the incoming message
    
    Arguments:
        data {bytes} -- the incoming message in byte form
    
    Returns:
        string/bytes -- if a answer is needed it is simply returned
    '''

    global running
    # Success
    if data == Signals.OK:
        pass
    
    # Permission denied
    elif data == Signals.WRONG_PWD:
        print(Bcolors.FAIL + "wrong password" + Bcolors.ENDC)
        running = False
        
    
    # pwd requested
    elif data == Signals.PWD_REQUEST:
        return pwd


    # authentication successful
    elif data == Signals.RIGHT_PWD:
        print(Bcolors.OKBLUE + "\rauthenticated" + Bcolors.ENDC, end = "\n-> ")
        Client.is_authenticated = True

    # server quit
    elif data == Signals.QUIT or data == b'':
        Client.close_all()
        running = False
        # os._exit(1)
         
    # benchmark
    elif data == Signals.TIME:
        print("msg recived at: ", time.time())

        
    #unexpected
    else:
        print(Bcolors.WARNING + "\runexpected data: {}".format(data) + Bcolors.ENDC, end = "\n-> ")
            

Client = Sockets.HandleSockets("127.0.0.1", 1337, "admin", mode = "c", on_message = on_message)
Client.isDaemon = True
Client.start()


# get user input
try:
    while running:
        i = input("\r-> ")
        # parse for commands
        if i == "q":
            Client.close_all()
            exit()
        # send if no command was found
        elif not Sockets.no_connection:
            Client.send(i)

except:
    Client.close_all()
    os._exit(1)
