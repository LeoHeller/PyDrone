import time, os, signals, sys, Sockets
from signals import Bcolors, Signals


pwd = "admin"
running = True

def on_message(data):
        #0 = Success
    if data == Signals.OK:
        pass
    
    #13 = Permission denied
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
         
    #unexpected
    else:
        print(Bcolors.WARNING + "\runexpected data: {}".format(data) + Bcolors.ENDC, end = "\n-> ")
            

Client = Sockets.HandleSockets("127.0.0.1", 1337, "admin", mode = "c", on_message = on_message)
Client.isDaemon = True
Client.start()



try:
    while running:
        i = input("\r-> ")
        if i == "q":
            Client.close_all()
            os._exit(1)
        elif not Sockets.no_connection:
            Client.send(i)

except:
    Client.close_all()
    os._exit(1)