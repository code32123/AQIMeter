# Imports from python and pip
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, os, json

# Imports from custom programs
from getAQI import getAQI
from Tools import * 

# The main window of the meter itself
class Window(QWidget):
	def __init__(self):
		try: # Reads the settings file, loads the JSON, then sets variables based on the JSON
			with open("settings.json", "r") as f:
				self.data = f.read()
			self.data = json.loads(self.data)
			url = self.data["link"]
			BGColor = self.data["background-color"]
			Color = self.data["color"]
		except:	# If no file is found, or there's a problem, revert to default values, and log event
			LoggerPrint("File 'settings.json' not found. Using default settings. To fix, run the settings program.", "Warning")
			url = "https://www.airnow.gov/?city=Eugene&state=OR&country=USA"
			BGColor = "white"
			Color = "black"

		# Setup the window
		QMainWindow.__init__(self, None, (Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))
		self.setAttribute(Qt.WA_TranslucentBackground)
		# For draggability functions
		self.mousePos = None
		# Set the title
		self.setWindowTitle("AQI")
		# Getting the AQI
		AQI = getAQI(url)
		# Creating a label widget and styling it
		self.Meter = QLabel(str(AQI), self)
		self.Meter.setFont(QFont('Arial', 18))
		# Sets the border color depending on the AQI
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
		# Moves the meter to the upper left hand corner of the invisible window
		self.Meter.move(0, 0)
		# Sets the meters size to wrap the text
		self.Meter.adjustSize()
		# Sets the meter text to the current AQI and re-checks the border color
		def update_label():
			AQI = getAQI(url)
			self.Meter.setText(str(AQI))
			self.Meter.adjustSize()
			updateColor(AQI)

		# Begins a loop that will update the meter every 5 minutes
		self.timer = QTimer()
		self.timer.timeout.connect(update_label)
		self.timer.start(5*(60000))  # every 5 * 60,000 milliseconds, or 5 minute

	# Mouse events for dragging
	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.mousePos = event.pos() # While mouse is down, save it's position

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.mousePos = None # When mouse is up, delete it's saved postition

	def mouseMoveEvent(self, event):
		if self.mousePos: # If the position isn't None when the mouse is moved:
			self.move(self.pos() + (event.pos() - self.mousePos)) # Then move the window to wherever the mouse is


# If this program is run directly, generate the meter. If imported, don't
if __name__ == '__main__':
	# Create pyqt5 app
	App = QApplication(sys.argv)

	# Create the instance of our Window
	window = Window()

	# Show it
	window.show()

	# Start the app
	sys.exit(App.exec())
