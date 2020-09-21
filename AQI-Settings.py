from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor

from Tools import *
import json
import AQIMeter

class program(QWidget): 
	def __init__(self): 
		QMainWindow.__init__(self, None)
		try:
			with open("settings.json", "r") as f:
				self.data = f.read()
			self.data = json.loads(self.data)
			self.styles = {
			  "background-color"	: self.data["background-color"],
			  "color"				: self.data["color"],
			}
		except:
			self.styles = {
			  "background-color"	: "white",
			  "color"				: "black",
			}
			
		self.locations = {
			"Eugene, OR":"https://www.airnow.gov/?city=Eugene&state=OR&country=USA",
			"Boardman, OR" :"https://www.airnow.gov/?city=Boardman&state=OR&country=USA",
			"Other" :"Other",
		}
		self.link = "https://www.airnow.gov/?city=Eugene&state=OR&country=USA"
		self.setWindowTitle("AQI - Settings")
		self.left = 500
		self.top = 300
		self.width = 320
		self.height = 150
		self.initUI()
	
	def initUI(self):
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.locationComboBox = QComboBox()
		self.locationComboBox.addItems(self.locations.keys())
		self.locationComboBox.activated[str].connect(self.changeLocation)

		self.locationOptional = QLineEdit(self)
		self.locationOptional.hide()

		self.locationOptionalSubmitButton = QPushButton("Done", self)
		self.locationOptionalSubmitButton.clicked.connect(self.locationOptionalSubmit)
		self.locationOptionalSubmitButton.hide()

		self.locationComboBoxLable = QLabel("Location:")
		self.locationComboBoxLable.setBuddy(self.locationComboBox)

		self.backgroundColorPickerButton = QPushButton('Background Color', self)
		self.backgroundColorPickerButton.clicked.connect(self.backgroundColorPicker)

		self.colorPickerButton = QPushButton('Foreground Color', self)
		self.colorPickerButton.clicked.connect(self.colorPicker)

		self.transparentBackgroundCheckBox = QCheckBox("Transparent BG")
		self.transparentBackgroundCheckBox.setChecked(False)
		self.transparentBackgroundCheckBox.toggled.connect(self.backgroundTransparent)

		self.transparentCheckBox = QCheckBox("Transparent FG")
		self.transparentCheckBox.setChecked(False)
		self.transparentCheckBox.toggled.connect(self.foregroundTransparent)

		self.DemoMeter = QLabel("00", self)
		self.DemoMeter.setFont(QFont('Arial', 18))
		self.updateSyles()

		self.saveButton = QPushButton('SAVE', self)
		self.saveButton.clicked.connect(self.save)

		self.launchButton = QPushButton('Launch!', self)
		self.launchButton.clicked.connect(self.launch)

		self.hLayout1 = QHBoxLayout()
		self.hLayout1.addWidget(self.transparentBackgroundCheckBox)
		self.hLayout1.addWidget(self.backgroundColorPickerButton)

		self.hLayout2 = QHBoxLayout()
		self.hLayout2.addWidget(self.transparentCheckBox)
		self.hLayout2.addWidget(self.colorPickerButton)

		self.hLayout3 = QHBoxLayout()
		self.hLayout3.addWidget(self.locationComboBoxLable)
		self.hLayout3.addWidget(self.locationComboBox)

		self.hLayout4 = QHBoxLayout()
		self.hLayout4.addWidget(self.locationOptional)
		self.hLayout4.addWidget(self.locationOptionalSubmitButton)

		self.hLayout5 = QHBoxLayout()
		self.hLayout5.insertSpacing(0, 250)
		self.hLayout5.addWidget(self.DemoMeter)

		self.vLayout = QVBoxLayout()
		self.vLayout.addLayout(self.hLayout1)
		self.vLayout.addLayout(self.hLayout2)
		self.vLayout.addLayout(self.hLayout3)
		self.vLayout.addLayout(self.hLayout4)
		self.vLayout.addLayout(self.hLayout5)
		self.vLayout.addWidget(self.saveButton)
		self.vLayout.addWidget(self.launchButton)
		self.vLayout.insertSpacing(4, 50)
		self.setLayout(self.vLayout)

		self.show()

	def locationOptionalSubmit(self):
		locationOptionalText = self.locationOptional.text()
		self.link = locationOptionalText
		MyPrint(self.link, "Debug")	

	def changeLocation(self, string):
		self.link = self.locations[string]
		if string == "Other":
			self.locationOptionalSubmitButton.show()
			self.locationOptional.show()
		else:
			self.locationOptionalSubmitButton.hide()
			self.locationOptional.hide()
		MyPrint(self.link, "Debug")

	def updateSyles(self):
		stylesString = ""
		for key, value in self.styles.items():
			stylesString += key + ":" + value + ";"
		self.DemoMeter.setStyleSheet(stylesString + "border:3px solid green;border-radius:5px;")
		self.DemoMeter.adjustSize() 

	def backgroundTransparent(self, checked):
		self.backgroundColorPickerButton.setDisabled(checked)
		if checked:
			self.oldBGColor = self.styles["background-color"]
			self.styles["background-color"] = "transparent"
		else:
			self.styles["background-color"] = self.oldBGColor
		self.updateSyles()

	def foregroundTransparent(self, checked):
		self.colorPickerButton.setDisabled(checked)
		if checked:
			self.oldFGColor = self.styles["color"]
			self.styles["color"] = "transparent"
		else:
			self.styles["color"] = self.oldFGColor
		self.updateSyles()

	def launch(self):
		#App2 = QApplication(sys.argv) 
		window = AQIMeter.Window()
		window.show()
		#sys.exit(App2.exec())
		pass

	def save(self):
		with open("settings.json", "w+") as f:
			tempArray = self.styles
			tempArray["link"] = self.link
			f.write(json.dumps(tempArray))

	def backgroundColorPicker(self):
		color = QColorDialog.getColor()

		if color.isValid():
			MyPrint(color.name(), "Debug")
			self.styles["background-color"] = color.name()
			self.updateSyles()

	def colorPicker(self):
		color = QColorDialog.getColor()

		if color.isValid():
			MyPrint(color.name(), "Debug")
			self.styles["color"] = color.name()
			self.updateSyles()


if __name__ == '__main__':
	App = QApplication(sys.argv)
	program = program()
	sys.exit(App.exec())