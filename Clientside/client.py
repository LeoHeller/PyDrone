import socket, sys, threading, os, time
from signals import Signals, Bcolors
pwd  = "admin"

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1337        # The port used by the server



    



running = True
is_authenticated = False

def get_server(s):
    global running, is_authenticated
    while running:
        data = s.recv(1024)
        # TCP codes: https://gist.github.com/gabrielfalcao/4216897

        #0 = Success
        if data == Signals.OK:
            pass
        
        #13 = Permission denied
        elif data == Signals.WRONG_PWD:
            print(Bcolors.FAIL + "wrong password" + Bcolors.ENDC)
            running = False
            break
        
        # pwd requested
        elif data == Signals.PWD_REQUEST:
            s.sendall(pwd.encode())
            print("password sent")
            continue

        # authentication successful
        elif data == Signals.RIGHT_PWD:
            print(Bcolors.OKBLUE + "authenticated" + Bcolors.ENDC)
            is_authenticated = True

        # server quit
        elif data == Signals.QUIT or data == b'':
            print("\nserver quit, quitting")
            s.close()
            running = False
            # os._exit(1)
            break 
        #unexpected
        else:
            print(Bcolors.WARNING + "\nunexpected data: ",data + Bcolors.ENDC)
            continue

    os._exit(1)

try:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        t = threading.Thread(target=get_server, args=(s,))
        t.isDaemon = True
        t.start()

        while not is_authenticated:
            time.sleep(0.1)
        while running:
            i = input("->")
            if i == "q":
                s.close()
                running = False
                os._exit(1)
                break
            if i == "Left":
                s.sendall(Signals.LEFT)
                print("going left")
            
            else:
                s.sendall(i.encode())
        
except KeyboardInterrupt:
    s.close()
    print("disconnected")
    os._exit(1)  