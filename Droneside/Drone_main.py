import time, os, sys
sys.path.insert(0, '/home/leo/Desktop/PyDrone/modules/')


from signals import Signals, Bcolors
import Sockets, utils
import cProfile


 
utils.update = "Sun Oct  7 11:27:34 2018"
utils.head()


pwd = "admin"
global running
running = True

def on_message(data):
    global running
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
        Server.is_authenticated = True

    # server quit
    elif data == Signals.QUIT or data == b'':
        Sockets.no_connection = True
         
    #unexpected
    else:
        print(Bcolors.WARNING + "\runexpected data: {}".format(data) + Bcolors.ENDC, end = "\n-> ")
            


Server = Sockets.HandleSockets("127.0.0.1", 1337, "admin", mode = "s", on_message = on_message)
Server.isDaemon = True
Server.start()

try:
    while running:
        i = input("\r-> ")
        if i == "q":
            Server.close_all()
            Sockets.should_be_running = False
            exit()
            Server.join()
            print("server joined")
            running = False
            #os._exit(1)
        if i == "b": # benchmark
            Server.send(Signals.TIME)
            print(time.time())

        elif not Sockets.no_connection:
            Server.send(i)

except:
    Server.close_all()
    os._exit(1)


