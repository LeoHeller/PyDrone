import socket, utils, time, sys
from signals import Signals, Bcolors




class Handle_Sockets():
    def __init__(self, ip, port, password):
        '''simple wrapper for sockets to create a interface between the drone and client
        
        Arguments:
            ip {string} -- ip to wich others should connect
            port {int} -- port onto wich others should connect
            password {string} -- password that clients enter when connecting
        '''

        self.ip = ip
        self.port = port
        self.password = password

        self.no_client_connected = True

        self.sock = self.setup_sockets()
        self.mainloop()

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

    def mainloop(self):
        '''main loop for reciving and sending data
        '''

        try:
            while self.no_client_connected:
                self.conn, self.addr = self.sock.accept()
                if self.authenticate():
                    pass
                else:
                    self.no_client_connected = True
                    continue


                while True:
                    data = self.conn.recv(1024)
                    if data == b'':
                        print(Bcolors.OKBLUE + "client disconnected" + Bcolors.ENDC)
                        break
                    else:
                        try:
                            self.on_message()
                        except AttributeError as e:
                            print(e)
                            print(Bcolors.WARNING + "on_message not set, please set it with 'Handle_Sockets.on_message = my_on_messagefunction'" + Bcolors.ENDC)
                            print("new data from user: ", data)
                    self.conn.sendall(Signals.OK)
        except KeyboardInterrupt:
            self.close_all()

    def close_all(self):
        if not self.no_client_connected:
            self.conn.sendall(Signals.QUIT)
            self.conn.close()
            self.sock.close()

    def send(self, msg):
        self.conn.sendall(msg)


def main():
    utils.setupdate()
    utils.head()

if __name__ == '__main__':
    main()

