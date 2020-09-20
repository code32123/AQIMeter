# importing the required libraries 
  
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import sys 

from getAQI import getAQI
from Tools import *

  
class Window(QMainWindow): 
	def __init__(self,BorderColor="white"): 
		QMainWindow.__init__(self, None, (Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.__press_pos = None
		self.setStyleSheet("background-color: white; border: 2px solid " + BorderColor + ";border-radius:5px;")
		# set the title 
		self.setWindowTitle("AQI")
		self.setWindowOpacity(1) 
		# creating a label widget 
		AQI = getAQI()
		self.Meter = QLabel(str(AQI), self) 
		self.Meter.setFont(QFont('Arial', 18))
		def updateColor(AQI):
			if   0 <= AQI <=  50:
				self.Meter.setStyleSheet("background-color: white; border: 2px solid green       ;border-radius:5px;")
			if  50 <= AQI <= 100:
				self.Meter.setStyleSheet("background-color: white; border: 2px solid yellow      ;border-radius:5px;")
			if 100 <= AQI <= 150:
				self.Meter.setStyleSheet("background-color: white; border: 2px solid orange      ;border-radius:5px;")
			if 150 <= AQI <= 200:
				self.Meter.setStyleSheet("background-color: white; border: 2px solid red         ;border-radius:5px;")
			if 200 <= AQI <= 300:
				self.Meter.setStyleSheet("background-color: white; border: 2px solid mediumorchid;border-radius:5px;")
			if 300 < AQI:
				self.Meter.setStyleSheet("background-color: white; border: 2px solid maroon      ;border-radius:5px;")
		updateColor(AQI)
		# moving position 
		self.Meter.move(0, 0) 
		self.Meter.adjustSize() 
		# show all the widgets 
		self.show()
		self.setMouseTracking(True)
		def update_label():
			AQI = getAQI()
			self.Meter.setText(str(AQI))
			updateColor(AQI)


		self.timer = QTimer()
		self.timer.timeout.connect(update_label)
		self.timer.start(5*(60000))  # every 5 * 60,000 milliseconds, or 5 minute

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.__press_pos = event.pos()  # remember starting position

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.__press_pos = None

	def mouseMoveEvent(self, event):
		if self.__press_pos:  # follow the mouse
			self.move(self.pos() + (event.pos() - self.__press_pos))
  
# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = Window() 
  
# start the app 
sys.exit(App.exec())