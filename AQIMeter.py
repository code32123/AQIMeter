# importing the required libraries 
  
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import sys, os 

from getAQI import getAQI
from Tools import *
import json

#main window of the meter itself
class Window(QWidget): 
	def __init__(self):
		try:
			#Reads the settings file, loads the JSON, then sets variables based on the JSON
			with open("settings.json", "r") as f:
				self.data = f.read()
			self.data = json.loads(self.data)
			url = self.data["link"]
			BGColor = self.data["background-color"]
			Color = self.data["color"]
		except:
			LoggerPrint("File 'settings.json' not found. Using default settings. To fix, run the settings program.", "Warning")
			url = "https://www.airnow.gov/?city=Eugene&state=OR&country=USA"
			BGColor = "white"
			Color = "black"


		QMainWindow.__init__(self, None, (Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.__press_pos = None
		self.setStyleSheet("background-color: "+BGColor+"; border: 2px solid white; border-radius:5px;color: "+Color+";")
		# set the title 
		self.setWindowTitle("AQI")
		self.setWindowOpacity(1) 
		# creating a label widget 
		AQI = getAQI(url)
		self.Meter = QLabel(str(AQI), self) 
		self.Meter.setFont(QFont('Arial', 18))
		def updateColor(AQI):
			beginning = "background-color: "+BGColor+"; border: 3px solid "
			ending = ";border-radius:5px;color:"+Color+";"
			if   0 <= AQI <=  50:
				self.Meter.setStyleSheet(beginning + "green       " + ending)
			if  50 <= AQI <= 100:
				self.Meter.setStyleSheet(beginning + "yellow      " + ending)
			if 100 <= AQI <= 150:
				self.Meter.setStyleSheet(beginning + "orange      " + ending)
			if 150 <= AQI <= 200:
				self.Meter.setStyleSheet(beginning + "red         " + ending)
			if 200 <= AQI <= 300:
				self.Meter.setStyleSheet(beginning + "mediumorchid" + ending)
			if 300 < AQI:
				self.Meter.setStyleSheet(beginning + "maroon      " + ending)
		updateColor(AQI)
		# moving position 
		self.Meter.move(0, 0) 
		self.Meter.adjustSize() 
		self.setMouseTracking(True)
		def update_label():
			AQI = getAQI(url)
			self.Meter.setText(str(AQI))
			self.Meter.adjustSize() 
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
  


if __name__ == '__main__':
	# create pyqt5 app 
	App = QApplication(sys.argv) 
	  
	# create the instance of our Window 
	window = Window() 
	window.show()
	  
	# start the app 
	sys.exit(App.exec())