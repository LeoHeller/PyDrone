"""
Sockets lib using TCP sockets.

Main class HandleSockets instantiates a listener and sender class.

__author__ = "Leo Heller"
__copyright__ = "None"
__credits__ = ["Leo Heller", "Stack Overflow"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Leo Heller"
__status__ = "Development
"""
import socket
import sys
import time
import threading
import queue

sys.path.insert(0, '../modules/')  # noqa
try:
    import PyQt5
    from PyQt5 import QtCore

    PyQt5_imported = True
except ImportError:
    PyQt5_imported = False

from signals import Bcolors, Signals


def _on_message(msg):
    """Overruled by users on_message function.

    Default on_message function called if none is defined by the user.

    Arguments:
        msg {bytes} -- incoming data sent by the other end
    """
    print("\r" + "new data from user: ", msg, end="\n-> ")


def ping(host, port):
    """Ping a host and port to see if a sockets server is running."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.25)
            s.connect((host, port))
            s.sendall(Signals.PING_RQST)
            data = s.recv(1024)
            if data == Signals.PING:
                return True
            else:
                print(data)

        s.close()
    except (ConnectionRefusedError, ConnectionResetError, socket.timeout, OSError):
        return False
    else:
        return True


no_connection = True
should_be_running = True


# noinspection PyUnresolvedReferences
class HandleSockets(PyQt5.QtCore.QThread if PyQt5_imported else threading.Thread):
    """Wrapper for sockets to create a interface between the drone and client."""

    def __init__(self, ip, port, password, on_message, mode="s"):
        """Initialize class with arguments.

        Arguments:
            ip {string} -- ip to which others should connect
            port {int} -- port onto which others should connect
            password {string} -- password that clients enter when connecting
            mode {string} -- "c" for client, "s" for server
            on_message {function} -- function that should be called when a new message comes in.
            should have one argument, to which the raw byte string is passed
        """
        # global variables to tell the threads when to stop and when to try to reconnect
        global no_connection, should_be_running
        # call thread init
        PyQt5.QtCore.QThread.__init__(self) if PyQt5_imported else threading.Thread.__init__(self)

        # arguments used to start class
        self.ip = ip
        self.port = port
        self.password = password
        self.mode = mode
        self.on_message = on_message

        self.listener, self.sender, self.conn, self.connected_device_address = None, None, None, None

        self.isDaemon = True

        # either start as 'c' client or as 's' server
        if self.mode == "c":
            self.sock = self.setup_client_socket()
        elif self.mode == "s":
            self.sock = self.setup_server_sockets()
        # make sure the user chose a valid choice
        else:
            print("\r" + Bcolors.WARNING + "please use a valid mode, 'c' or 's'. (not {})".format(
                self.mode) + Bcolors.ENDC, end="\n-> ")
            exit()

    if PyQt5_imported:
        def __del__(self):
            """Is required by QThread."""
            self.wait()

    @staticmethod
    def setup_client_socket():
        """Create a socket object for further use by the client application.

        Returns:
            object -- a socket object

        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s

    def setup_server_sockets(self):
        """Create a socket object for further use by the server.

        Returns:
            object -- a socket object

        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        s.listen(2)

        return s

    def accept(self):
        """Accept any incoming clients."""
        global no_connection
        # accept the client
        self.conn, self.connected_device_address = self.sock.accept()

        # create a new 'sender' thread that sends out any enqueued messages
        self.sender = Sender(self.conn, self.mode, self)
        self.sender.isDaemon = True
        self.sender.start()

        no_connection = False

        # validate the client
        if not self.authenticate():
            self.close_all()
            no_connection = True
        else:
            # create a new 'listener' thread that listens for any new messages
            self.listener = Listener(self.conn, self)
            self.listener.isDaemon = True
            self.listener.start()

    def connect(self):
        """Connect to the server."""
        global no_connection, should_be_running
        try:
            # try to connect, if no server is running a exception wil be thrown and catched
            self.sock.connect((self.ip, self.port))
            no_connection = False

            # create a new 'listener' thread that listens for any new messages
            self.sender = Sender(self.sock, self.mode, self)
            self.sender.isDaemon = True
            self.sender.start()

            # create a new 'sender' thread that sends out any enqueued messages
            self.listener = Listener(self.sock, self)
            self.listener.isDaemon = True
            self.listener.start()

            print("\r" + Bcolors.OKBLUE + "connected, waiting for authorisation request" + Bcolors.ENDC, end="\n-> ")

        except (ConnectionRefusedError, OSError):
            # catch any problems if no server is running or the socket obj has expired
            print(
                f"\r{Bcolors.FAIL} Connection refused, check if a server is running on the specified host and port.{Bcolors.ENDC}",
                end="")
            no_connection = True

    def run(self):
        """Reconnect to the server/accept any clients."""
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
            time.sleep(0.01)

    def authenticate(self):
        """When the client connects they are asked to authenticate themselves.

        Returns:
            bool -- if the authentication is successful True is returned

        """
        global no_connection, should_be_running
        if not should_be_running:
            return
        # send other end a request for a password
        # wait 0.1 sec for other side to start up
        time.sleep(0.2)

        self.send(Signals.PWD_REQUEST)

        data = self.conn.recv(1024)

        # check if the password is correct
        if data == Signals.PING_RQST:
            print("\r" + Bcolors.OKGREEN + "ping received from {}".format(self.connected_device_address) + Bcolors.ENDC)
            self.conn.sendall(Signals.PING)
            self.conn.close()
            return False
        if data.decode() != self.password:
            # if it is not send the signal that it was wrong and disconnect the client
            print("\r" + Bcolors.FAIL + "permission denied to {}".format(self.connected_device_address) + Bcolors.ENDC)
            try:
                self.conn.sendall(Signals.WRONG_PWD)
                self.conn.shutdown(socket.SHUT_RDWR)
                self.conn.close()
            except OSError:
                pass
            return False

        else:
            # let the client know the password was correct and allow him to continue on
            self.conn.sendall(Signals.RIGHT_PWD)
            print(
                "\r" + Bcolors.OKBLUE + "permission granted to {}".format(self.connected_device_address) + Bcolors.ENDC)
            no_connection = False
            return True

    def close_all(self, _exit=True):
        """Clean up function for sockets."""
        global should_be_running, no_connection
        # if we are connected
        if not no_connection:
            # tell the other end we are quitting
            try:
                self.send(Signals.QUIT)
            except Exception:
                pass
            self.sock.close()
            print("\r" + Bcolors.OKBLUE + "disconnecting" + Bcolors.ENDC)

            should_be_running = False
            no_connection = True

            if _exit:
                exit()
            # exit()

        else:
            no_connection = True
            should_be_running = False
        print("\r" + Bcolors.OKBLUE + "closed connections" + Bcolors.ENDC)

    def send(self, msg):
        """Send messages using this Wrapper.

        Appends the message to the stack so it can be sent.
        Catch the message if no client/server is present

        Arguments:
            msg {string/bytes} -- message to be sent.
            Can be bytes or a string as it will be converted to bytes later
        """
        if not no_connection:
            self.sender.queue.put(msg)
        else:
            if not should_be_running:
                print("\r" + Bcolors.WARNING + "no client connected" + Bcolors.ENDC, end="\n-> ")


class Listener(PyQt5.QtCore.QThread if PyQt5_imported else threading.Thread):
    """Thread that listens to new messages from the other side and calls the on_message function."""

    if PyQt5_imported:
        msg_signal = PyQt5.QtCore.pyqtSignal(bytes)

    def __init__(self, conn, hs):
        """Initialize Thread."""
        PyQt5.QtCore.QThread.__init__(self) if PyQt5_imported else threading.Thread.__init__(self)

        self.conn = conn
        self.hs = hs

    if PyQt5_imported:
        def __del__(self):
            """Is requred by QThread."""
            self.wait()

    def run(self):
        """Mainloop of the Listner Thread. Collects any new messages."""
        global no_connection, should_be_running
        print("\r" + Bcolors.OKBLUE + "Listener Started" + Bcolors.ENDC, end="\n-> ")

        # recive data while a client is connected
        while not no_connection and should_be_running is True:
            try:
                data = self.conn.recv(1024)
            except ConnectionResetError:
                no_connection = True
                return

            try:
                # execute userdefined on_message function or emit a signal and send its output
                try:
                    self.msg_signal.emit(data)
                except Exception:
                    pass
                try:
                    self.hs.send(self.hs.on_message(data))
                except Exception:
                    # print(e)
                    pass
            except AttributeError as e:
                # catch any errors if the user forgot to define on_message correctly
                print(e)
                print(
                    Bcolors.WARNING + "on_message not set, please set it in the servers arguments" + Bcolors.ENDC)
                # default on_message function, just prints the output as a warning.
                _on_message(data)

        print("\r" + Bcolors.OKBLUE + "Listener Stopped" + Bcolors.ENDC, end="\n-> ")


class Sender(PyQt5.QtCore.QThread if PyQt5_imported else threading.Thread):
    """Send messages from a stack."""

    def __init__(self, conn, mode, hs):
        """Initialize Thread."""
        PyQt5.QtCore.QThread.__init__(self) if PyQt5_imported else threading.Thread.__init__(self)

        global no_connection, should_be_running
        self.conn = conn
        self.mode = mode
        self.hs = hs
        self.stack = []
        self.queue = queue.Queue()
        print("\r" + Bcolors.OKBLUE + "Sender Started" + Bcolors.ENDC, end="\n-> ")

    if PyQt5_imported:
        def __del__(self):
            """Is required by QThread."""
            self.wait()

    def run(self):
        """Mainloop of the Sender Thread."""
        while not no_connection and should_be_running:
            # if a connection is present send data
            if not no_connection:
                self._send()
            time.sleep(0.05)

        print("\r" + Bcolors.OKBLUE + "Sender Stopped" + Bcolors.ENDC, end="\n-> ")

    def _send(self):
        """Send message from stack. Only for Internal use."""
        global should_be_running
        # only send data if there is data to be sent and it should be sent
        data = self.queue.get()
        if data is not None and should_be_running and not no_connection:
            packet = data
            if type(packet) != bytes:
                self.conn.sendall(packet.encode())
            else:
                self.conn.sendall(packet)

        # if len(self.stack) > 0 and self.stack[-1] is not None and should_be_running and not no_connection:
        #     packet = self.stack.pop()
        #     if type(packet) != bytes:
        #         self.conn.sendall(packet.encode())
        #     else:
        #         self.conn.sendall(packet)
