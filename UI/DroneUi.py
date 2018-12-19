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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(639, 0))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidgetPage1 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tabWidgetPage1.sizePolicy().hasHeightForWidth())
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
        self.Chat.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Chat.setReadOnly(True)
        self.Chat.setPlaceholderText("")
        self.Chat.setObjectName("Chat")
        self.ConnectButton = QtWidgets.QPushButton(self.tabWidgetPage1)
        self.ConnectButton.setGeometry(QtCore.QRect(500, 290, 100, 27))
        self.ConnectButton.setFlat(False)
        self.ConnectButton.setObjectName("ConnectButton")
        self.ServerInput = QtWidgets.QLineEdit(self.tabWidgetPage1)
        self.ServerInput.setGeometry(QtCore.QRect(309, 290, 181, 27))
        self.ServerInput.setInputMask("")
        self.ServerInput.setText("")
        self.ServerInput.setObjectName("ServerInput")
        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tabWidgetPage2 = QtWidgets.QWidget()
        self.tabWidgetPage2.setObjectName("tabWidgetPage2")
        self.elevation_label = QtWidgets.QLabel(self.tabWidgetPage2)
        self.elevation_label.setGeometry(QtCore.QRect(30, 40, 91, 31))
        self.elevation_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.elevation_label.setAlignment(QtCore.Qt.AlignCenter)
        self.elevation_label.setObjectName("elevation_label")
        self.height_label = QtWidgets.QLabel(self.tabWidgetPage2)
        self.height_label.setGeometry(QtCore.QRect(30, 110, 91, 31))
        self.height_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.height_label.setAlignment(QtCore.Qt.AlignCenter)
        self.height_label.setObjectName("height_label")
        self.lcdNumber_elevation = QtWidgets.QLCDNumber(self.tabWidgetPage2)
        self.lcdNumber_elevation.setGeometry(QtCore.QRect(150, 45, 64, 23))
        self.lcdNumber_elevation.setObjectName("lcdNumber_elevation")
        self.lcdNumber_height = QtWidgets.QLCDNumber(self.tabWidgetPage2)
        self.lcdNumber_height.setGeometry(QtCore.QRect(150, 115, 64, 23))
        self.lcdNumber_height.setObjectName("lcdNumber_height")
        self.speed_label = QtWidgets.QLabel(self.tabWidgetPage2)
        self.speed_label.setGeometry(QtCore.QRect(30, 210, 91, 31))
        self.speed_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.speed_label.setObjectName("speed_label")
        self.lcdNumber_speed = QtWidgets.QLCDNumber(self.tabWidgetPage2)
        self.lcdNumber_speed.setGeometry(QtCore.QRect(150, 215, 64, 23))
        self.lcdNumber_speed.setObjectName("lcdNumber_speed")
        self.tabWidget.addTab(self.tabWidgetPage2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 27))
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
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "PyDrone Control 1.0"))
        self.ChatText.setText(_translate("MainWindow", "You:"))
        self.ConnectButton.setText(_translate("MainWindow", "Connect"))
        self.ServerInput.setPlaceholderText(
            _translate("MainWindow", "127.0.0.1:1337"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tabWidgetPage1), _translate("MainWindow", "Chat"))
        self.elevation_label.setToolTip(_translate(
            "MainWindow", "Height from the ground in meters"))
        self.elevation_label.setText(_translate("MainWindow", "Elevation [m]"))
        self.height_label.setToolTip(_translate(
            "MainWindow", "Height from the sea level in meters"))
        self.height_label.setText(_translate("MainWindow", "Height [m]"))
        self.speed_label.setToolTip(_translate(
            "MainWindow", "Height from the sea level in meters"))
        self.speed_label.setText(_translate("MainWindow", "Speed [m/s]"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tabWidgetPage2), _translate("MainWindow", "Stats"))