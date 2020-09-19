# importing the required libraries 
  
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import sys 

from getAQI import getAQI
  
  
class Window(QMainWindow): 
  
  
	def __init__(self): 
		QMainWindow.__init__(self, None, (Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.__press_pos = None

		self.setStyleSheet("background-color: white; border: 2px solid red;")
  
		# set the title 
		self.setWindowTitle("AQI")
  
		self.setWindowOpacity(1) 
  
  
		# setting  the geometry of window 
		self.setGeometry(0, 0, 80, 50) 
  
		# creating a label widget 
		self.label_1 = QLabel(str(getAQI()), self) 

		self.label_1.setFont(QFont('Arial', 18))

		# moving position 
		self.label_1.move(20, 10) 
  
		self.label_1.adjustSize() 
  
		# show all the widgets 
		self.show()

		self.setMouseTracking(True)

		def update_label():
			self.label_1.setText(str(getAQI()))

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