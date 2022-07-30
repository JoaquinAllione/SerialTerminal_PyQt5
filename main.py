import sys 
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5.QtGui import QColor
from UI_SERIAL_Terminal import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

import resources_rc

class MiApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.port = QSerialPort() 

		self.baudratesDIC = {
		'1200':1200,
		'2400':2400,
		'4800':4800,
		'9600':9600,
		'19200':19200,
		'38400':38400,
		'57600':57600,
		'115200':115200
		}
	
		self.ui.comboBox_baudrate.addItems(self.baudratesDIC.keys())
		self.ui.comboBox_baudrate.setCurrentText('9600')
		self.ui.pushButton_disconnect.setEnabled(False)
		self.ui.pushButton_connect.setEnabled(True)

		self.update_ports()
		
		#Events
		self.ui.pushButton_connect.clicked.connect(self.connect_serial)
		self.ui.pushButton_disconnect.clicked.connect(self.disconnect_serial)
		self.ui.pushButton_send.clicked.connect(self.send_data)
		self.ui.pushButton_refresh.clicked.connect(self.update_ports)
		self.ui.pushButton_clean.clicked.connect(self.clear_terminal)
		self.ui.lineEdit_data.returnPressed.connect(self.send_data)
		self.port.readyRead.connect(self.update_terminal)

	def update_terminal(self):
		if not self.port.canReadLine(): return
		rx = self.port.readLine()
		data = str(rx, 'utf-8').strip()
		self.ui.textBrowser_terminal_view.setTextColor(QColor.fromRgb(255,255,255))
		self.ui.textBrowser_terminal_view.append('<<' + ' ' + data)

	def disconnect_serial(self):
		if self.port.isOpen():
			self.port.close()
			self.ui.textBrowser_terminal_view.setTextColor(QColor.fromRgb(250,50,50))
			self.ui.textBrowser_terminal_view.append('>> ' + 'PORT DISCONNECTED' + ' <<')
			self.ui.pushButton_disconnect.setEnabled(False)
			self.ui.pushButton_connect.setEnabled(True)

	def connect_serial(self):		
		try:
			port = self.ui.comboBox_port_list.currentText()
			baud = self.ui.comboBox_baudrate.currentText()
			self.port.setBaudRate(int(baud))
			self.port.setPortName(port)
			if self.port.open(QtCore.QIODevice.ReadWrite):
				self.ui.textBrowser_terminal_view.setTextColor(QColor.fromRgb(50, 190, 166))
				self.ui.textBrowser_terminal_view.append('>> ' + 'CONNECTED TO ' + port + ' <<')
				self.ui.pushButton_disconnect.setEnabled(True)
				self.ui.pushButton_connect.setEnabled(False)
		except:
			self.ui.textBrowser_terminal_view.setTextColor(QColor.fromRgb(250,50,50))
			self.ui.textBrowser_terminal_view.append('>> ' + 'ERROR OCURRED!' + ' <<')
		finally:
			pass
		

	def send_data(self):
		try:
			if self.port.isOpen():
				data = self.ui.lineEdit_data.text() + '\n'
				self.port.write(data.encode())
				self.ui.textBrowser_terminal_view.setTextColor(QColor.fromRgb(50,50,50))
				self.ui.textBrowser_terminal_view.append('>>' + ' ' + self.ui.lineEdit_data.text())
			else:
				self.ui.textBrowser_terminal_view.setTextColor(QColor.fromRgb(250,50,50))
				self.ui.textBrowser_terminal_view.append('>> ' + 'DEVICE NOT OPEN' + ' <<')
		except:
			self.ui.textBrowser_terminal_view.setTextColor(QColor.fromRgb(250,50,50))
			self.ui.textBrowser_terminal_view.append('>> ' + 'ERROR OCURRED!' + ' <<')
		finally:
			pass
		


	def update_ports(self):
		self.ui.comboBox_port_list.clear()
		self.ui.comboBox_port_list.addItems([ port.portName() for port in QSerialPortInfo().availablePorts() ])

	def clear_terminal(self):
		self.ui.textBrowser_terminal_view.clear()

	def closeEvent(self,e):
		if self.port.isOpen():
			self.port.close()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = MiApp()
	w.show()
	sys.exit(app.exec_())