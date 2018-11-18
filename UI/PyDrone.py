import sys, time, socket
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from DroneUi import Ui_MainWindow

sys.path.insert(0, '/home/leo/Desktop/PyDrone/modules/')

import Sockets
import utils
from signals import Bcolors, Signals






class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()



       

        # connect buttons and other ui elements
        self.ui.ChatInput.returnPressed.connect(self.ui_send)
        self.ui.ConnectButton.clicked.connect(self.connect_to_server)
        self.ui.ServerInput.returnPressed.connect(self.connect_to_server)
        

    #@PyQt5.QtCore.pyqtSlot()
    def on_message(self,msg):
        if msg == b'':
            msg = "quit"
        else:
            self.ui.Chat.setText(self.ui.Chat.toPlainText() + "\ndrone: " + str(msg))

            print(msg)


    def connect_to_server(self):
        #
         
        if not self.check_host(self.ui.ServerInput.text()):
            
            msgBox = PyQt5.QtWidgets.QMessageBox()
            msgBox.setText("Please enter a valid host.")
            msgBox.exec_()
            print("thats not right")
        else:
            ip, port = self.check_host(self.ui.ServerInput.text())
            self.Client = Sockets.HandleSockets(ip, port, "admin", mode = "c" , on_message = None)
            self.Client.isDaemon = True
            self.Client.start()
            time.sleep(0.01)
            # connect the on_message signal from Sockets.py to a function
            self.Client.listener.msg_signal.connect(self.on_message)
    
    def check_host(self, host):
        # parse and check host
        # example: 192.168.2.1:111 --> '192.168.2.1', 111
        # example: myserver.com:111 --> 'myserversip', 111

        if host == "": host = "localhost:1337"


        # catch wrong format for host
        if ':' not in host:
            return False
        port = host.split(":")[1]
        host = host.split(":")[0]

        # check if port is a int and in the valid port range
        try:
            port = int(port)
        except ValueError:
            return False
        # check if port is valid
        if port not in range(65535): return False
        # check if host exits
        try:
            host = socket.gethostbyname(host)
        except socket.gaierror:
            return False

        return host, port


    def ui_send(self):
        self.Client.send(self.ui.ChatInput.text())
        self.ui.Chat.setText(self.ui.Chat.toPlainText() + "\nyou: " + self.ui.ChatInput.text())
        self.ui.ChatInput.clear()



app = QApplication(sys.argv)



w = AppWindow()
w.show()
sys.exit(app.exec_())
