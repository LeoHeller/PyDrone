import sys, time, socket
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from DroneUi import Ui_MainWindow

sys.path.insert(0, '/home/leo/Desktop/PyDrone/modules/')

import Sockets
import utils
from signals import Bcolors, Signals




test = {Signals.WRONG_PWD : "WRONG_PWD", Signals.RIGHT_PWD : "RIGHT_PWD", Signals.PING : "PING" ,Signals.PWD_REQUEST : "PWD_REQUEST", Signals.OK : "OK", Signals.QUIT : "QUIT"}





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


		#self.ui.ChatText.ensureCursorVisible()


	#@PyQt5.QtCore.pyqtSlot()
	def on_message(self,msg):
		if msg in test:
			msg = test[msg]
		if msg == b'' or msg == Signals.QUIT and Sockets.no_connection == False:
			msg = "quit"
			if Sockets.should_be_running:
				self.ui.Chat.append("drone: " + str(msg))
				Sockets.should_be_running = False
				Sockets.no_connection = True
				#time.sleep(0.02)
				self.Client.close_all()

		else:
			self.ui.Chat.append("drone: " + str(msg))


	def connect_to_server(self):
		if Sockets.no_connection:
			# is the input in a valid format?
			ip, port = self.check_host(self.ui.ServerInput.text())

			if (ip,port) == (None,None):

				msgBox = PyQt5.QtWidgets.QMessageBox()
				msgBox.setText("Please enter a valid host.")
				msgBox.exec_()



			elif Sockets.ping(ip,port):

				Sockets.should_be_running = True
				Sockets.no_connection = True
				self.Client = Sockets.HandleSockets(ip, port, "admin", mode = "c" , on_message = None)
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
				msgBox.setText("Please check if a server is running on the specified host.")
				msgBox.exec_()


	def check_host(self, host):
		# parse and check host
		# example: 192.168.2.1:111 --> '192.168.2.1', 111
		# example: myserver.com:111 --> 'myserversip', 111

		if host == "": host = "localhost:1337"


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
		if port not in range(65535): return None, None
		# check if host exits
		try:
			host = socket.gethostbyname(host)
		except socket.gaierror:
			return None, None
		# port is open and a server is running
		return host, port




	def ui_send(self):
		self.Client.send(self.ui.ChatInput.text())
		self.ui.Chat.append("you: " + self.ui.ChatInput.text())
		self.ui.ChatInput.clear()



app = QApplication(sys.argv)



w = AppWindow()
w.show()
sys.exit(app.exec_())
