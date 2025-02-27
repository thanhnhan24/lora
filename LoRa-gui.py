# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loraTfTidj.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
import socket
import threading
import datetime

class TCPClientThread(QThread):
    data_received = Signal(str)
    connection_lost = Signal(str)

    def __init__(self, ip, port=5000):
        super().__init__()
        self.ip = ip
        self.port = port
        self.running = True
        self.client_socket = None

    def run(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.ip, self.port))
            while self.running:
                data = self.client_socket.recv(1024)
                if data:
                    self.data_received.emit(data.decode('utf-8'))
        except Exception as e:
            self.data_received.emit(f"Error: {str(e)}")

    def stop(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()

class ClockThread(QThread):
    time_updated = Signal(str, str)
    
    def run(self):
        while True:
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M:%S")
            date_str = now.strftime("%d/%m/%Y")
            self.time_updated.emit(time_str, date_str)
            self.msleep(1000)  # Cập nhật mỗi giây

class Ui_MainWindow(object):
    def __init__(self):
        self.tcp_thread = None
        self.clock_thread = ClockThread()
        self.clock_thread.time_updated.connect(self.time_updated)
        self.clock_thread.start()
        self.model1 = None
        
        pass

    def time_updated(self, time_str, date_str):
        self.realtime_clk.setPlainText(time_str)
        self.realtime_cld.setPlainText(date_str)

    def start_tcp_connection(self):
        try:
            ip = self.IP_Address.toPlainText().strip()
            if not ip:
                self.update_log("Please enter a valid IP address.")
                return

            if self.tcp_thread:
                self.tcp_thread.stop()
                self.tcp_thread.wait()

            self.tcp_thread = TCPClientThread(ip)
            self.tcp_thread.data_received.connect(self.display_received_data)
            self.tcp_thread.start()
            self.update_log(f"Connecting to {ip}...")
        except Exception as e:
            self.update_log(f"Error: {str(e)}")

    def display_received_data(self, data):
        self.update_log(f"Received: {data}")

    def update_log(self, message):
        now = datetime.datetime.now()
        current = now.strftime("%H:%M:%S")
        message = f"[{current}]: {message}"
        item = QStandardItem(message)
        self.model1.insertRow(0, item)
        pass

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1447, 808)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(60, 80, 431, 501))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.IP_Address = QPlainTextEdit(self.groupBox)
        self.IP_Address.setObjectName(u"IP_Address")
        self.IP_Address.setGeometry(QRect(10, 30, 261, 51))
        self.IP_Address.setOverwriteMode(True)
        self.Connect_button = QPushButton(self.groupBox)
        self.Connect_button.setObjectName(u"Connect_button")
        self.Connect_button.setGeometry(QRect(280, 30, 141, 51))
        self.groupBox_3 = QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 100, 411, 81))
        self.horizontalLayoutWidget = QWidget(self.groupBox_3)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 30, 391, 51))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.contactor_on = QPushButton(self.horizontalLayoutWidget)
        self.contactor_on.setObjectName(u"contactor_on")

        self.horizontalLayout.addWidget(self.contactor_on)

        self.contactor_off = QPushButton(self.horizontalLayoutWidget)
        self.contactor_off.setObjectName(u"contactor_off")

        self.horizontalLayout.addWidget(self.contactor_off)

        self.groupBox_4 = QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 200, 411, 81))
        self.horizontalLayoutWidget_2 = QWidget(self.groupBox_4)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 30, 391, 51))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.light_on = QPushButton(self.horizontalLayoutWidget_2)
        self.light_on.setObjectName(u"light_on")

        self.horizontalLayout_2.addWidget(self.light_on)

        self.light_off = QPushButton(self.horizontalLayoutWidget_2)
        self.light_off.setObjectName(u"light_off")

        self.horizontalLayout_2.addWidget(self.light_off)

        self.groupBox_5 = QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(10, 300, 411, 81))
        self.horizontalLayoutWidget_3 = QWidget(self.groupBox_5)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 30, 391, 51))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.socket_on = QPushButton(self.horizontalLayoutWidget_3)
        self.socket_on.setObjectName(u"socket_on")

        self.horizontalLayout_3.addWidget(self.socket_on)

        self.socket_off = QPushButton(self.horizontalLayoutWidget_3)
        self.socket_off.setObjectName(u"socket_off")

        self.horizontalLayout_3.addWidget(self.socket_off)

        self.groupBox_6 = QGroupBox(self.groupBox)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(10, 400, 411, 81))
        self.horizontalLayoutWidget_4 = QWidget(self.groupBox_6)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(10, 30, 391, 51))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.projector_on = QPushButton(self.horizontalLayoutWidget_4)
        self.projector_on.setObjectName(u"projector_on")

        self.horizontalLayout_4.addWidget(self.projector_on)

        self.projector_off = QPushButton(self.horizontalLayoutWidget_4)
        self.projector_off.setObjectName(u"projector_off")

        self.horizontalLayout_4.addWidget(self.projector_off)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(530, 80, 891, 431))
        self.groupBox_2.setFont(font)
        self.tabWidget = QTabWidget(self.groupBox_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 30, 871, 381))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.groupBox_8 = QGroupBox(self.tab)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setGeometry(QRect(10, 10, 240, 91))
        self.temprature1 = QPlainTextEdit(self.groupBox_8)
        self.temprature1.setObjectName(u"plainTextEdit_4")
        self.temprature1.setGeometry(QRect(10, 30, 221, 51))
        self.groupBox_9 = QGroupBox(self.tab)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setGeometry(QRect(10, 110, 241, 91))
        self.gas1 = QPlainTextEdit(self.groupBox_9)
        self.gas1.setObjectName(u"plainTextEdit_5")
        self.gas1.setGeometry(QRect(10, 30, 221, 51))
        self.groupBox_11 = QGroupBox(self.tab)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setGeometry(QRect(270, 10, 240, 91))
        self.humidity1 = QPlainTextEdit(self.groupBox_11)
        self.humidity1.setObjectName(u"plainTextEdit_9")
        self.humidity1.setGeometry(QRect(10, 30, 221, 51))
        self.groupBox_10 = QGroupBox(self.tab)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setGeometry(QRect(270, 110, 241, 91))
        self.power_consumtion1 = QPlainTextEdit(self.groupBox_10)
        self.power_consumtion1.setObjectName(u"plainTextEdit_8")
        self.power_consumtion1.setGeometry(QRect(10, 30, 221, 51))
        self.groupBox_13 = QGroupBox(self.tab)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setGeometry(QRect(530, 10, 240, 91))
        self.uv1 = QPlainTextEdit(self.groupBox_13)
        self.uv1.setObjectName(u"plainTextEdit_11")
        self.uv1.setGeometry(QRect(10, 30, 221, 51))
        self.groupBox_12 = QGroupBox(self.tab)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setGeometry(QRect(530, 110, 241, 91))
        self.rssi1 = QPlainTextEdit(self.groupBox_12)
        self.rssi1.setObjectName(u"plainTextEdit_10")
        self.rssi1.setGeometry(QRect(10, 30, 221, 51))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.groupBox_14 = QGroupBox(self.tab_2)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setGeometry(QRect(530, 10, 240, 91))
        self.plainTextEdit_12 = QPlainTextEdit(self.groupBox_14)
        self.plainTextEdit_12.setObjectName(u"plainTextEdit_12")
        self.plainTextEdit_12.setGeometry(QRect(10, 30, 221, 51))
        self.groupBox_15 = QGroupBox(self.tab_2)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setGeometry(QRect(270, 110, 241, 91))
        self.plainTextEdit_13 = QPlainTextEdit(self.groupBox_15)
        self.plainTextEdit_13.setObjectName(u"plainTextEdit_13")
        self.plainTextEdit_13.setGeometry(QRect(10, 30, 221, 51))
        self.groupBox_16 = QGroupBox(self.tab_2)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.groupBox_16.setGeometry(QRect(530, 110, 241, 91))
        self.plainTextEdit_14 = QPlainTextEdit(self.groupBox_16)
        self.plainTextEdit_14.setObjectName(u"plainTextEdit_14")
        self.plainTextEdit_14.setGeometry(QRect(10, 30, 221, 51))
        self.groupBox_17 = QGroupBox(self.tab_2)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.groupBox_17.setGeometry(QRect(270, 10, 240, 91))
        self.plainTextEdit_15 = QPlainTextEdit(self.groupBox_17)
        self.plainTextEdit_15.setObjectName(u"plainTextEdit_15")
        self.plainTextEdit_15.setGeometry(QRect(10, 30, 221, 51))
        self.groupBox_18 = QGroupBox(self.tab_2)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.groupBox_18.setGeometry(QRect(10, 110, 241, 91))
        self.plainTextEdit_6 = QPlainTextEdit(self.groupBox_18)
        self.plainTextEdit_6.setObjectName(u"plainTextEdit_6")
        self.plainTextEdit_6.setGeometry(QRect(10, 30, 221, 51))
        self.groupBox_19 = QGroupBox(self.tab_2)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.groupBox_19.setGeometry(QRect(10, 10, 240, 91))
        self.plainTextEdit_7 = QPlainTextEdit(self.groupBox_19)
        self.plainTextEdit_7.setObjectName(u"plainTextEdit_7")
        self.plainTextEdit_7.setGeometry(QRect(10, 30, 221, 51))
        self.log_output = QListView(self.centralwidget)
        self.log_output.setObjectName(u"listView")
        self.log_output.setGeometry(QRect(530, 530, 891, 221))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 20, 1361, 31))
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(17)
        font1.setBold(True)
        font1.setWeight(75)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.groupBox_7 = QGroupBox(self.centralwidget)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(60, 590, 431, 161))
        font2 = QFont()
        font2.setFamily(u"Arial")
        font2.setPointSize(29)
        font2.setBold(True)
        font2.setWeight(75)
        self.groupBox_7.setFont(font)
        self.realtime_clk = QPlainTextEdit(self.groupBox_7)
        self.realtime_clk.setFont(font2)
        self.realtime_clk.setObjectName(u"realtime_clk")
        self.realtime_clk.setGeometry(QRect(10, 30, 411, 71))
        self.realtime_cld = QPlainTextEdit(self.groupBox_7)
        self.realtime_cld.setObjectName(u"realtime_cld")
        self.realtime_cld.setGeometry(QRect(10, 110, 411, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1447, 26))
        self.menuLoRa = QMenu(self.menubar)
        self.menuLoRa.setObjectName(u"menuLoRa")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuLoRa.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0110i\u1ec1u khi\u1ec3n", None))
        self.IP_Address.setDocumentTitle("")
        self.IP_Address.setPlainText("")
        self.IP_Address.setPlaceholderText(QCoreApplication.translate("MainWindow", u"IP Gateway", None))
        self.Connect_button.setText(QCoreApplication.translate("MainWindow", u"CONNECT", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Contactor", None))
        self.contactor_on.setText(QCoreApplication.translate("MainWindow", u"ON", None))
        self.contactor_off.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u0110\u00e8n", None))
        self.light_on.setText(QCoreApplication.translate("MainWindow", u"ON", None))
        self.light_off.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u1ed4 \u0111i\u1ec7n", None))
        self.socket_on.setText(QCoreApplication.translate("MainWindow", u"ON", None))
        self.socket_off.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"M\u00e1y chi\u1ebfu", None))
        self.projector_on.setText(QCoreApplication.translate("MainWindow", u"ON", None))
        self.projector_off.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Gi\u00e1m s\u00e1t", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Nhi\u1ec7t \u0111\u1ed9", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"GAS", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"\u0110\u1ed9 \u1ea9m", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"\u0110i\u1ec7n n\u0103ng ti\u00eau th\u1ee5", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"UV", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"RSSI", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Node 1", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"UV", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("MainWindow", u"\u0110i\u1ec7n n\u0103ng ti\u00eau th\u1ee5", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("MainWindow", u"RSSI", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("MainWindow", u"\u0110\u1ed9 \u1ea9m", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("MainWindow", u"GAS", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("MainWindow", u"Nhi\u1ec7t \u0111\u1ed9", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Node 2", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Giao di\u1ec7n \u0111i\u1ec1u khi\u1ec3n v\u00e0 gi\u00e1m s\u00e1t h\u1ec7 th\u1ed1ng LoRa", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Real time clock", None))
        self.realtime_clk.setPlainText(QCoreApplication.translate("MainWindow", u"111", None))
        self.menuLoRa.setTitle(QCoreApplication.translate("MainWindow", u"LoRa", None))
    # retranslateUi

    

class ConsoleMainWindow(QMainWindow):
    def __init__(self):
        super(ConsoleMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Connect_button.clicked.connect(self.ui.start_tcp_connection)
        self.ui.model1 = QStandardItemModel()
        self.ui.log_output.setModel(self.ui.model1)
    pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = ConsoleMainWindow()
    mainwin.show()
    sys.exit(app.exec_())