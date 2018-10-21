# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyDrone.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(640, 480)
		font = QtGui.QFont()
		font.setFamily("Roboto")
		MainWindow.setFont(font)
		MainWindow.setUnifiedTitleAndToolBarOnMac(False)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 641, 431))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.tabWidget = QtWidgets.QTabWidget(self.gridLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
		self.tabWidget.setSizePolicy(sizePolicy)
		self.tabWidget.setMinimumSize(QtCore.QSize(639, 0))
		self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.tabWidget.setAutoFillBackground(False)
		self.tabWidget.setObjectName("tabWidget")
		self.tabWidgetPage1 = QtWidgets.QWidget()
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.tabWidgetPage1.sizePolicy().hasHeightForWidth())
		self.tabWidgetPage1.setSizePolicy(sizePolicy)
		self.tabWidgetPage1.setObjectName("tabWidgetPage1")
		self.ChatInput = QtWidgets.QLineEdit(self.tabWidgetPage1)
		self.ChatInput.setGeometry(QtCore.QRect(90, 290, 181, 25))
		self.ChatInput.setObjectName("ChatInput")
		self.ChatText = QtWidgets.QLabel(self.tabWidgetPage1)
		self.ChatText.setGeometry(QtCore.QRect(10, 290, 67, 17))
		self.ChatText.setObjectName("ChatText")
		self.Chat = QtWidgets.QTextBrowser(self.tabWidgetPage1)
		self.Chat.setGeometry(QtCore.QRect(80, 20, 501, 181))
		self.Chat.setReadOnly(True)
		self.Chat.setObjectName("Chat")
		self.tabWidget.addTab(self.tabWidgetPage1, "")
		self.tabWidgetPage2 = QtWidgets.QWidget()
		self.tabWidgetPage2.setObjectName("tabWidgetPage2")
		self.tabWidget.addTab(self.tabWidgetPage2, "")
		self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 26))
		self.menubar.setAutoFillBackground(False)
		self.menubar.setDefaultUp(False)
		self.menubar.setNativeMenuBar(True)
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "PyDrone Control 1.0"))
		self.ChatText.setText(_translate("MainWindow", "You:"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), _translate("MainWindow", "test2"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage2), _translate("MainWindow", "Test"))


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

