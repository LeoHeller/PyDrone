import cProfile
import os
import socket
import sys
import threading
import time

sys.path.insert(0, '/home/leo/Desktop/PyDrone/modules/')
from signals import Bcolors, Signals



global no_connection, should_be_running
no_connection = True
should_be_running = True



def _on_message(msg):
    '''Default on_message method, should be overruled by users on_method.
    
    Arguments:
        msg {bytes} -- incoming data sent by the other end
    '''

    print("\r" + "new data from user: ", msg, end = "\n-> ")




import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog





class HandleSockets(PyQt5.QtCore.QThread):
    def __init__(self, ip, port, password, on_message, mode = "s"):
        '''simple wrapper for sockets to create a interface between the drone and client

        Arguments:
            ip {string} -- ip to wich others should connect
            port {int} -- port onto wich others should connect
            password {string} -- password that clients enter when connecting
            mode {string} -- "c" for client, "s" for server
            on_message {function} -- function that should be called when a new message comes in. should have one argument, to which the raw byte string is passed
        '''
        # global [description]variables to tell the threads when to stop and when to try to reconnect
        global no_connection, should_be_running
        # call thread init
        PyQt5.QtCore.QThread.__init__(self)


        # arguments used to start class
        self.ip = ip
        self.port = port
        self.password = password
        self.mode = mode
        self.on_message = on_message

        # either start as 'c' client or as 's' server
        if mode == "c":
            self.sock = self.setup_client_socket()
        elif mode == "s":
            self.sock = self.setup_server_sockets()
        # make sure the user chose a valid choice
        else:
            print("\r" + Bcolors.WARNING + "please use a valid mode, 'c' or 's'. (not {})".format(self.mode) + Bcolors.ENDC, end = "\n-> ")
            exit()


    def __del__(self):
        self.wait()


    def setup_client_socket(self):
        '''creates a socket object for further use by the client application
        
        Returns:
            object -- a socket object
        '''

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        return s

    def setup_server_sockets(self):
        '''creates a socket object for further use by the server
        
        Returns:
            objec -- a socket object
        '''

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        s.listen(2)

        return s

    def accept(self):
        '''accept any incoming clients
        '''

        global no_connection
        # accept the client
        self.conn, self.addr = self.sock.accept()
        # validate the client
        if self.authenticate():
            
            # create a new 'listener' thread that listens for any new messages
            self.listener = Listener(self.conn, self)
            self.listener.isDaemon = True
            self.listener.start()

            # create a new 'sender' thread that sends out any enqueued messages
            self.sender = Sender(self.conn)
            self.sender.isDaemon = True
            self.sender.start()

            no_connection = False
        else:
            no_connection = True


    def connect(self):
        '''connect to the server
        '''

        global no_connection
        try:
            # try to connect, if no server is running a exception wil be thrown and catched
            self.sock.connect((self.ip, self.port))
            no_connection = False
            
            # create a new 'listener' thread that listens for any new messages
            self.sender = Sender(self.sock)
            self.sender.isDaemon = True
            self.sender.start()

            # create a new 'sender' thread that sends out any enqueued messages
            self.listener = Listener(self.sock, self)
            self.listener.isDaemon = True
            self.listener.start()

            print("\r" + Bcolors.OKBLUE + "connected, wating for authorisation request" + Bcolors.ENDC, end = "\n-> ")
            

        except (ConnectionRefusedError, OSError):
            # catch any problems if no server is running or the socket obj has expired
            print("\r" + Bcolors.FAIL + "Connection refused, check if a server is running on the specified host and port." + Bcolors.ENDC, end = "\n-> ")
            no_connection = True
        # wait 0.1 seconds until the next try
        time.sleep(0.1)


    def run(self):
        '''reconnect to the server/accept any clients
        '''

        global should_be_running, no_connection
        while should_be_running:
            while no_connection:
                if self.mode == "s":
                    # accept a client
                    self.accept()

                if self.mode == "c":
                    # reconnect to the server
                    self.connect()
            # wait before trying again
            time.sleep(0.1)



  
    def authenticate(self):

        '''when the client connects he is asked to authenticate himself.

        Returns:
            bool -- if the authentication is successful True is returned
        '''
        global no_connection, should_be_running
        if not should_be_running:
            return
        # send other end a request for a password
        # wait 0.1 sec for other side to start up
        time.sleep(0.1)
        self.conn.sendall(Signals.PWD_REQUEST)
        givenpwd = self.conn.recv(1024)

        # check if the password is correct
        if givenpwd.decode() != self.password:
            # if it is not send the signal that it was wrong and disconnect the client
            print("\r" + Bcolors.FAIL + "permission denied to {}".format(self.addr) + Bcolors.ENDC)
            self.conn.sendall(Signals.WRONG_PWD)
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()
            return False

        else:
            # let the client know the password was correct and allow him to continue on
            self.conn.sendall(Signals.RIGHT_PWD)
            print("\r" + Bcolors.OKBLUE + "permission granted to {}".format(self.addr) + Bcolors.ENDC)
            no_connection = False
            return True

    def close_all(self):
        '''clean up function for sockets
        '''

        global should_be_running, no_connection
        if not no_connection:
            # tell the other end we are quitting
            self.send(Signals.QUIT)
            self.sock.close()
            print("\r" + Bcolors.OKBLUE + "disconnecting" + Bcolors.ENDC)

            should_be_running = False             
            no_connection = True

            exit()
            #exit()

        else:
            no_connection = True
            should_be_running = False 
        print("\r" + Bcolors.OKBLUE + "closed connections" + Bcolors.ENDC)
        


    def send(self, msg):
        '''wrapper for sending messages.
        appends the message to the stack so it can be sent.
        catch the message if no client/server is present
        
        Arguments:
            msg {string/bytes} -- message to be sent. Can be bytes or a string as it will be converted to bytes later
        '''


        if not no_connection:
            self.sender.stack.append(msg)
        else:
            if not should_be_running:
                print("\r" + Bcolors.WARNING + "no client connected" + Bcolors.ENDC, end = "\n-> ")




class Listener(PyQt5.QtCore.QThread):
    '''Thread that listens to new messages from the other side and calls the on_message function
    '''
    msg_signal = PyQt5.QtCore.pyqtSignal(bytes)

    def __init__(self, conn, hs):
        PyQt5.QtCore.QThread.__init__(self)

        self.conn = conn
        self.hs = hs

    def __del__(self):
        self.wait()

    def run(self):
        # runs in the thread
        global no_connection, should_be_running
        print("\r" + Bcolors.OKBLUE + "Listener Started" + Bcolors.ENDC, end = "\n-> ")

        # recive data while a client is connected
        while not no_connection and should_be_running == True:
            data = self.conn.recv(1024)

            try:
                # execute userdefined on_message function or emit a signal and send its output
                try:
                    self.msg_signal.emit(data)
                except Exception as e:
                    print("280", e)
                try:
                    self.hs.send(self.hs.on_message(data))
                except Exception as e:
                    pass

            except AttributeError as e:
                # catch any errors if the user forgot to define on_message correctly
                print(e)
                print(Bcolors.WARNING + "on_message not set, please set it in the servers arguments" + Bcolors.ENDC)
                # default on_message function, just prints the output as a warning.
                _on_message(data)
        
        print("\r" + Bcolors.OKBLUE + "Listener Stopped" + Bcolors.ENDC, end = "\n-> ")


class Sender(PyQt5.QtCore.QThread):
    '''send messages from a stack
    '''

    def __init__(self, conn):
        PyQt5.QtCore.QThread.__init__(self)

        global no_connection, should_be_running
        self.conn = conn
        self.stack = []
        print("\r" + Bcolors.OKBLUE + "Sender Started" + Bcolors.ENDC, end = "\n-> ")

    def __del__(self):
        self.wait()


    def run(self):
        while not no_connection and should_be_running:
            # if a connection is present send data
            if not no_connection:
                self._send()
            time.sleep(0.1)

        print("\r" + Bcolors.OKBLUE + "Sender Stopped" + Bcolors.ENDC, end = "\n-> ")


    def _send(self):
        global should_be_running
        # only send data if there is data to be sent and it should be sent
        if len(self.stack) > 0 and self.stack[-1] != None and should_be_running:
            packet = self.stack.pop()
            if type(packet) != bytes:
                self.conn.sendall(packet.encode())
            else:
                self.conn.sendall(packet)
        else:
            pass
