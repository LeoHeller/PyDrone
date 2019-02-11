import wireframe_cube
"""
User interface for controlling the drone.

Uses PyQt5 to create the Ui, values are passed to a instance of Sockets.HandleSockets

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
sys.path.insert(0, '../modules/')  # noqa


from DroneUi import Ui_MainWindow

import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow

import Sockets

import signals
from signals import Signals


test = {Signals.WRONG_PWD: "WRONG_PWD", Signals.RIGHT_PWD: "RIGHT_PWD", Signals.PING: "PING",
        Signals.PWD_REQUEST: "PWD_REQUEST", Signals.OK: "OK", Signals.QUIT: "QUIT"}


class AppWindow(QMainWindow):
    """QMainWindow subclass, used for UI."""

    def __init__(self, sim):
        """Set up the ui."""
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.keyPressEvent = self.OnKeyPressEvent
        # self.keyReleaseEvent = self.OnKeyReleaseEvent
        self.show()

        # connect buttons and other ui elements
        self.ui.ChatInput.returnPressed.connect(self.ui_send)
        self.ui.ConnectButton.clicked.connect(self.connect_to_server)
        self.ui.ServerInput.returnPressed.connect(self.connect_to_server)
        self.ui.ThrustverticalSlider.valueChanged.connect(self.update_slider)
        self.ui.AbortpushButton.clicked.connect(self.Abort)
        self.ui.ArmpushButton.clicked.connect(self.Arm)
        self.ui.action192_168_10_1_1337.triggered.connect(lambda: self.connect_to_server("192.168.10.1:1337"))
        self.ui.action192_168_2_236_1337.triggered.connect(lambda: self.connect_to_server("192.168.2.236:1337"))
        # setup val1ues
        self.sim = sim

    def Abort(self):
        if Sockets.no_connection == True:
            msgBox = PyQt5.QtWidgets.QMessageBox()
            msgBox.setText("Please connect to a server first.")
            msgBox.exec_()
        else:
            self.Client.send(signals.Signals.QUIT)

    def Arm(self):
        if Sockets.no_connection == True:
            msgBox = PyQt5.QtWidgets.QMessageBox()
            msgBox.setText("Please connect to a server first.")
            msgBox.exec_()
        else:
            self.Client.send(signals.Signals.ARM)

    def update_slider(self, value):
        if Sockets.no_connection == True:
            msgBox = PyQt5.QtWidgets.QMessageBox()
            msgBox.setText("Please connect to a server first.")
            msgBox.exec_()
            self.ui.ThrustverticalSlider.setValue(0)
        else:
            value = int(value)
            if value > 100:
                value = 100
            if value < 0:
                value = 0

            self.ui.ThrustlcdNumber.display(value)
            self.ui.ThrustverticalSlider.setValue(value)
            self.Client.send(signals.Send.move_all(value))
            # print(self.ui.ThrustverticalSlider.value())

    def OnKeyPressEvent(self, event):
        if self.ui.tabWidget.currentIndex() is not 0:   # not in the controll tab > exit
            return

        if event.key() == 16777248:   # shift
            pass

        elif event.key() == 16777249:   # ctrl
            pass

        elif event.key() == 87:   # W
            self.update_slider(self.ui.ThrustverticalSlider.value()+1)

        elif event.key() == 65:   # A
            pass

        elif event.key() == 83:   # S
            self.update_slider(self.ui.ThrustverticalSlider.value()-1)

        elif event.key() == 68:   # D
            pass

        elif event.key() == 32:   # space
            self.Abort()

        # print(event.key())

    def on_message(self, msg):
        """Is called when a new message arrives."""

        if msg == b'' or msg == Signals.QUIT and Sockets.no_connection is False:
            msg = "quit"
            if Sockets.should_be_running:

                self.ui.Chat.append("drone: " + str(msg))
                Sockets.should_be_running = False
                Sockets.no_connection = True
                # time.sleep(0.02)
                self.Client.close_all()

        else:
            if msg in test:
                msg = test[msg]
            else:
                tel_data = signals.Recive.handle_input(msg)
                if tel_data is not None:
                    self.update_flight_data(*tel_data)
                    return

            self.ui.Chat.append("drone: " + str(msg))

    def connect_to_server(self, host=None):
        """Connect the client to the drone when the button is pressed."""
        if Sockets.no_connection:
            # is the input in a valid format?
            if host == None:
                ip, port = self.check_host(self.ui.ServerInput.text())
            else:
                ip, port = self.check_host(host)

            if (ip, port) == (None, None):

                msgBox = PyQt5.QtWidgets.QMessageBox()
                msgBox.setText("Please enter a valid host.")
                msgBox.exec_()

            elif Sockets.ping(ip, port):

                Sockets.should_be_running = True
                Sockets.no_connection = True
                self.Client = Sockets.HandleSockets(
                    ip, port, "admin", mode="c", on_message=None)
                self.Client.isDaemon = True
                self.Client.start()
                time.sleep(0.1)

                # when no server is running this thorws a error!
                try:
                    # connect the on_message signal from Sockets.py to a function
                    self.Client.listener.msg_signal.connect(self.on_message)
                except AttributeError:
                    self.Client.close_all()

            else:
                msgBox = PyQt5.QtWidgets.QMessageBox()
                msgBox.setText(
                    "Please check if a server is running on the specified host.")
                msgBox.exec_()

    def check_host(self, host):
        """
        Parse and check host.

        Arguments:
            host {str} -- host that should be validated

        Returns:
            (str, int) -- ip and port pair

        example: 192.168.2.1:111 --> '192.168.2.1', 111
        example: myserver.com:111 --> 'myserversip', 111

        """
        if host == "":
            host = "localhost:1337"

        # catch wrong format for host
        if ':' not in host:
            return None, None
        port = host.split(":")[1]
        host = host.split(":")[0]

        # check if port is a int and in the valid port range
        try:
            port = int(port)
        except ValueError:
            return None, None
        # check if port is valid
        if port not in range(65535):
            return None, None
        # check if host exits
        try:
            host = socket.gethostbyname(host)
        except socket.gaierror:
            return None, None
        # port is open and a server is running
        return host, port

    def ui_send(self):
        """Add message to stack and chat window."""
        if Sockets.no_connection:
            self.ui.Chat.append("failed to send, no connection")
            self.ui.ChatInput.clear()
            return

        msg = self.ui.ChatInput.text().lower()
        self.ui.ChatInput.clear()
        self.ui.Chat.append("you: " + str(msg))

        # parse input to check of commands
        if msg.startswith("move"):
            msg = signals.Send.move(
                int(msg.split(" ")[1]), int(msg.split(" ")[2]))
        elif "arm" in msg:
            msg = signals.Signals.ARM

        self.Client.send(msg)

    def update_flight_data(self, x, y, z):
        self.ui.lcdNumber_axis_x.display(x)
        self.ui.lcdNumber_axis_y.display(y)
        self.ui.lcdNumber_axis_z.display(z)

        self.sim.update(x, -y, z) # y, -z,


app = QApplication(sys.argv)

sim = wireframe_cube.Simulation()

w = AppWindow(sim)
w.show()

sys.exit(app.exec_())
