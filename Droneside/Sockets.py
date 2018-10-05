import socket, time, sys, threading, os
from signals import Signals, Bcolors


global no_connection
no_connection = True



def _on_message(msg):
    print("\r" + "new data from user: ", msg, end = "\n-> ")



class HandleSockets(threading.Thread):
    def __init__(self, ip, port, password, mode = "s", on_message = _on_message):
        '''simple wrapper for sockets to create a interface between the drone and client

        Arguments:
            ip {string} -- ip to wich others should connect
            port {int} -- port onto wich others should connect
            password {string} -- password that clients enter when connecting
            mode {string} -- "c" for client, "s" for server
            on_m {function} -- function that should be called when a new message comes in. should have one argument, to which the raw byte string is passed
        '''
        global no_connection
        # call thread init
        threading.Thread.__init__(self)

        self.ip = ip
        self.port = port
        self.password = password
        self.mode = mode
        self.on_message = on_message

        self.sock = self.setup_sockets()



    def setup_sockets(self):
        '''sets up a socket for further use


        Returns:
            socket -- socket object
        '''
        global no_connection
        # create socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set up the client
        if self.mode == "c":
            while no_connection:
                try:
                    self.s.connect((self.ip, self.port))
                    no_connection = False

                    self.sender = Sender(self.s)
                    self.sender.isDaemon = True
                    self.sender.start()

                    self.listener = Listener(self.s, self)
                    self.listener.isDaemon = True
                    self.listener.start()

                    print("\r" + Bcolors.OKBLUE + "connected, wating for authorisation request" + Bcolors.ENDC, end = "\n-> ")
                    continue

                except ConnectionRefusedError:
                    print("\r" + Bcolors.FAIL + "Connection refused, check if a server is running on the specified host and port." + Bcolors.ENDC, end = "\n-> ")
                    no_connection = True
                    #self.close_all()
                    #os._exit(1)
                time.sleep(0.1)


        # initiate Server
        if self.mode == "s":
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.ip, self.port))
            self.s.listen(2)
            try:
                while no_connection:
                    self.conn, self.addr = self.s.accept()
                    if self.authenticate():
                        self.listener = Listener(self.conn, self)
                        self.listener.isDaemon = True
                        self.listener.start()

                        self.sender = Sender(self.conn)
                        self.sender.isDaemon = True
                        self.sender.start()

                        no_connection = False
                    else:
                        no_connection = True
                        continue
            except KeyboardInterrupt:
                self.close_all()


        # return socket object
        return self.s

    def authenticate(self):

        '''when the client first connects he is asked to authenticate himself.

        Returns:
            bool -- if the authentication is successful True is returned
        '''
        global no_connection
        # send other end a request for a password
        self.conn.sendall(Signals.PWD_REQUEST)
        givenpwd = self.conn.recv(1024)

        # check if the password is correct
        if givenpwd.decode() != self.password:
            print("\r" + Bcolors.FAIL + "permission denied to {}".format(self.addr) + Bcolors.ENDC)
            self.conn.sendall(Signals.WRONG_PWD)
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()
            return False

        else:
            self.conn.sendall(Signals.RIGHT_PWD)
            print("\r" + Bcolors.OKBLUE + "permission granted to {}".format(self.addr) + Bcolors.ENDC)
            no_connection = False
            return True

    def close_all(self):
        # cleanup function
        global no_connection
        if not no_connection:
            #self.send(Signals.QUIT)
            self.s.close()
            print("\r" + Bcolors.OKBLUE + "disconnecting" + Bcolors.ENDC)
            os._exit(1)
        no_connection = True

    def send(self, msg):
        # adds the message to the stack to be sent
        if not no_connection:
            self.sender.stack.append(msg)
        else:
            print("\r" + Bcolors.WARNING + "no client connected" + Bcolors.ENDC, end = "\n-> ")


class Listener(threading.Thread):
    '''Thread that listens to output from the other side
    '''

    def __init__(self, conn, hs):
        threading.Thread.__init__(self)

        global no_connection
        self.conn = conn
        self.hs = hs

    def run(self):
        # runs in the thread
        global no_connection
        print("\r" + Bcolors.OKBLUE + "Listener Started" + Bcolors.ENDC, end = "\n-> ")
        # recive data while a client is connected
        while not no_connection:
            data = self.conn.recv(1024)

            try:
                # execute userdefined on_message function and send its output
                self.hs.send(self.hs.on_message(data))
            except AttributeError as e:
                # catch any errors if the user forgot to define on_message correctly
                print(e)
                print(Bcolors.WARNING + "on_message not set, please set it in the servers arguments" + Bcolors.ENDC)
                # default on_message function, just prints the output as a warning.
                _on_message(data)

class Sender(threading.Thread):
    '''send messages from a stack
    '''

    def __init__(self, conn):
        threading.Thread.__init__(self)

        global no_connection
        self.conn = conn
        self.stack = []
        print("\r" + Bcolors.OKBLUE + "Sender Started" + Bcolors.ENDC, end = "\n-> ")

    def run(self):
        while True:
            # if a client is connected send data
            if not no_connection:
                self._send()
            time.sleep(0.1)

    def _send(self):
        # only send data if there is data to be sent
        if len(self.stack) > 0 and self.stack[-1] != None:
            packet = self.stack.pop()
            if type(packet) != bytes:
                self.conn.sendall(packet.encode())
            else:
                self.conn.sendall(packet)
        else:
            pass





