import sys
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

        self.Client = Sockets.HandleSockets("127.0.0.1", 1337, "admin", mode = "c", on_message = self.on_message)
        self.Client.isDaemon = True
        self.Client.start()


        self.ui.ChatInput.returnPressed.connect(self.ui_send)



    def on_message(self, msg):
        if msg == b'':
            msg = "quit"
        print(msg)
        self.ui.Chat.setText(self.ui.Chat.toPlainText() + "\nServer: " + str(msg))

    def ui_send(self):
        self.send_recive.Client.send(self.ui.ChatInput.text())
        self.ui.Chat.setText(self.ui.Chat.toPlainText() + "\nyou: " + self.ui.ChatInput.text())
        self.ui.ChatInput.clear()



app = QApplication(sys.argv)



w = AppWindow()
w.show()
sys.exit(app.exec_())
