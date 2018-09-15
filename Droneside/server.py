import socket, utils, time, sys, threading
from signals import Signals, Bcolors


global no_client_connected
no_client_connected = True

class HandleSockets(threading.Thread):
    def __init__(self, ip, port, password):
        '''simple wrapper for sockets to create a interface between the drone and client
        
        Arguments:
            ip {string} -- ip to wich others should connect
            port {int} -- port onto wich others should connect
            password {string} -- password that clients enter when connecting
        '''
        global no_client_connected
        # call thread init
        threading.Thread.__init__(self)
        
        self.ip = ip
        self.port = port
        self.password = password

        self.sock = self.setup_sockets()

    def setup_sockets(self):
        '''sets up a socket for further use
        
        Returns:
            socket -- socket object
        '''

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        s.listen(2)

        return s

    def authenticate(self):
            '''when the client first connects he is asked to authenticate himself.
            
            Returns:
                bool -- if the authentication is successful True is returned
            '''

            self.conn.sendall(Signals.PWD_REQUEST)
            givenpwd = self.conn.recv(1024)


            if givenpwd.decode() != self.password:
                print(Bcolors.FAIL + "permission denied to {}".format(self.addr) + Bcolors.ENDC)
                self.conn.sendall(Signals.WRONG_PWD)
                self.conn.shutdown(socket.SHUT_RDWR)
                self.conn.close()
                return False
            else:
                self.conn.sendall(Signals.RIGHT_PWD)
                print(Bcolors.OKBLUE + "permission granted to {}".format(self.addr) + Bcolors.ENDC)
                return True

    def run(self):
        '''main loop for reciving and sending data
        '''
        global no_client_connected
        try:
            while no_client_connected:
                self.conn, self.addr = self.sock.accept()
                if self.authenticate():
                    listener = Listener(self.sock, self.conn)
                    listener.isDaemon = True
                    listener.start()

                    self.sender = Sender(self.sock, self.conn)
                    self.sender.isDaemon = True
                    self.sender.start()


                else:
                    no_client_connected = True
                    continue


                
                                      
        except KeyboardInterrupt:
            self.close_all()

    def close_all(self):
        global no_client_connected
        if not no_client_connected:
            self.conn.sendall(Signals.QUIT)
            self.conn.close()
            self.sock.close()
        no_client_connected = True

    def send(self, msg):
        self.sender.queue.append(msg)


class Listener(threading.Thread):
    def __init__(self, sock, conn):
        threading.Thread.__init__(self)

        global no_client_connected
        self.sock = sock
        self.conn = conn

    def run(self):
        global no_client_connected
        while not no_client_connected:
                    data = self.conn.recv(1024)
                    if data == b'':
                        print(Bcolors.OKBLUE + "client disconnected" + Bcolors.ENDC)
                        no_client_connected = True
                        break
                    else:
                        try:
                            self.on_message(data)
                        except AttributeError as e:
                            print(e)
                            print(Bcolors.WARNING + "on_message not set, please set it with 'Handle_Sockets.on_message = my_on_messagefunction'" + Bcolors.ENDC)
                            print("new data from user: ", data)
                    
    def on_message(self, message):
        self.conn.sendall(Signals.OK)

class Sender(threading.Thread):
    def __init__(self, sock, conn):
        threading.Thread.__init__(self)

        global no_client_connected
        self.sock = sock
        self.conn = conn
        self.queue = []

    def run(self):
        while no_client_connected:
            self._send() 

    def _send(self):
        if len(self.queue) > 0:
            self.conn.sendall(self.queue.pop().encode())
        
            print("special send")
        else:
            pass




def main():
    utils.setupdate()
    utils.head()

if __name__ == '__main__':
    main()

