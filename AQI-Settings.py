# Imports from python and pip
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
import sys, json

# Imports from custom programs
from Tools import *
import AQIMeter

# The main program
class program(QWidget): 
	def __init__(self): 
		# Init
		QMainWindow.__init__(self, None)

		try: # Reads the settings file, loads the JSON, then sets variables based on the JSON
			with open("settings.json", "r") as f:
				self.data = f.read()
			self.data = json.loads(self.data)
			self.link = self.data["link"]
			self.styles = {
			  "background-color"	: self.data["background-color"],
			  "color"				: self.data["color"],
			}
		except:	# If no file is found, or there's a problem, revert to default values
			self.styles = {
			  "background-color"	: "white",
			  "color"				: "black",
			}
			self.link = "https://www.airnow.gov/?city=Eugene&state=OR&country=USA"

		# Dict of location presets
		self.locations = {
			"Eugene, OR":"https://www.airnow.gov/?city=Eugene&state=OR&country=USA",
			"Boardman, OR" :"https://www.airnow.gov/?city=Boardman&state=OR&country=USA",
			"Spokane, WA" :"https://www.airnow.gov/?city=Spokane&state=WA&country=USA",
			"Murray, UT" :"https://www.airnow.gov/?city=Murray&state=UT&country=USA",
			"Other (see README)" :"Other",
		}

		# Sets the window title, and variables needed for initUI()
		self.setWindowTitle("AQI - Settings")
		self.left = 500
		self.top = 300
		self.width = 320
		self.height = 150
		self.initUI()
	
	def initUI(self):
		# Sets window size and position
		self.setGeometry(self.left, self.top, self.width, self.height)

		# UI Member: Location combo box of presets
		self.locationComboBox = QComboBox()
		self.locationComboBox.addItems(self.locations.keys())
		self.locationComboBox.activated[str].connect(self.changeLocation)

		# UI Member: Location label for above
		self.locationComboBoxLable = QLabel("Location:")
		self.locationComboBoxLable.setBuddy(self.locationComboBox)

		# UI Member: hidden for when someone selects "Other" so they can type it in, but it's not in the way
		self.locationOptional = QLineEdit(self)
		self.locationOptional.hide()

		# UI Member: Submit button for above
		self.locationOptionalSubmitButton = QPushButton("Done", self)
		self.locationOptionalSubmitButton.clicked.connect(self.locationOptionalSubmit)
		self.locationOptionalSubmitButton.hide()

		# UI Member: Color select button for background
		self.backgroundColorPickerButton = QPushButton('Background Color', self)
		self.backgroundColorPickerButton.clicked.connect(self.backgroundColorPicker)

		# UI Member: Transparent option for above
		self.transparentBackgroundCheckBox = QCheckBox("Transparent BG")
		self.transparentBackgroundCheckBox.setChecked(False)
		self.transparentBackgroundCheckBox.toggled.connect(self.backgroundTransparent)

		# UI Member: Color select button for foreground
		self.colorPickerButton = QPushButton('Foreground Color', self)
		self.colorPickerButton.clicked.connect(self.colorPicker)

		# UI Member: Transparent option for above
		self.transparentCheckBox = QCheckBox("Transparent FG")
		self.transparentCheckBox.setChecked(False)
		self.transparentCheckBox.toggled.connect(self.foregroundTransparent)

		# UI Member: Demo meter to display styling choices
		self.DemoMeter = QLabel("00", self)
		self.DemoMeter.setFont(QFont('Arial', 18))
		self.updateSyles()

		# UI Member: Save button
		self.saveButton = QPushButton('Save', self)
		self.saveButton.clicked.connect(self.save)

		# UI Member: Save and launch button
		self.launchButton = QPushButton('Save && Launch!', self)
		self.launchButton.clicked.connect(self.launch)

		# UI Member: Layouts for ourganization
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
		self.hLayout5.insertSpacing(0, 250) # The spacer is to squish the AQIMeter into the smallest shape that will wrap the text
		self.hLayout5.addWidget(self.DemoMeter)

		# UI Member: Applying all the H layouts to the one V layout
		self.vLayout = QVBoxLayout()
		self.vLayout.addLayout(self.hLayout1)
		self.vLayout.addLayout(self.hLayout2)
		self.vLayout.addLayout(self.hLayout3)
		self.vLayout.addLayout(self.hLayout4)
		self.vLayout.addLayout(self.hLayout5)
		self.vLayout.addWidget(self.saveButton)
		self.vLayout.addWidget(self.launchButton)
		self.vLayout.insertSpacing(4, 50) # The spacer is to squish the AQIMeter into the smallest shape that will wrap the text
		self.setLayout(self.vLayout)

		self.show()

	# This is run when the optional location link is submitted
	def locationOptionalSubmit(self):
		locationOptionalText = self.locationOptional.text()
		self.link = locationOptionalText
		LoggerPrint(self.link, "Debug")	

	# When someone selects a location, this save their choice as self.link
	def changeLocation(self, string):
		self.link = self.locations[string]
		if string == "Other" or self.locations[string] == "Other": # If "Other" is selected, show the text box to paste link
			self.locationOptionalSubmitButton.show()
			self.locationOptional.show()
		else:
			self.locationOptionalSubmitButton.hide() # Otherwise re-hide it
			self.locationOptional.hide()
		LoggerPrint(self.link, "Debug") # Log the link

	# Updates the styles when someone changes the dictionary
	def updateSyles(self):
		stylesString = ""
		for key, value in self.styles.items():
			stylesString += key + ":" + value + ";" # Loop through dict, adding styles to string
		self.DemoMeter.setStyleSheet(stylesString + "border:3px solid green;border-radius:5px;") # Add string to a constant style
		self.DemoMeter.adjustSize() # Probably unnecessary, but readjusts the size as needed.

	# Sets the background transparent and disables the color picker associated with it.
	def backgroundTransparent(self, checked):
		self.backgroundColorPickerButton.setDisabled(checked)
		if checked:
			self.oldBGColor = self.styles["background-color"]
			self.styles["background-color"] = "transparent"
		else:
			self.styles["background-color"] = self.oldBGColor
		self.updateSyles()

	# Sets the foreground transparent and disables the color picker associated with it.
	def foregroundTransparent(self, checked):
		self.colorPickerButton.setDisabled(checked)
		if checked:
			self.oldFGColor = self.styles["color"]
			self.styles["color"] = "transparent"
		else:
			self.styles["color"] = self.oldFGColor
		self.updateSyles()

	# Saves the settings and opens up the meter itself
	def launch(self):
		self.save()
		window = AQIMeter.Window()
		window.show()
		pass

	# Saves the styles and the link
	def save(self):
		with open("settings.json", "w+") as f:
			tempArray = self.styles
			tempArray["link"] = self.link
			f.write(json.dumps(tempArray))

	# Opens the background color picker
	def backgroundColorPicker(self):
		color = QColorDialog.getColor()

		if color.isValid():
			LoggerPrint(color.name(), "Debug")
			self.styles["background-color"] = color.name()
			self.updateSyles()

	# Opens the foreground color picker
	def colorPicker(self):
		color = QColorDialog.getColor()

		if color.isValid():
			LoggerPrint(color.name(), "Debug")
			self.styles["color"] = color.name()
			self.updateSyles()

# If this program is run directly, generate the meter. If imported, don't
if __name__ == '__main__':
	App = QApplication(sys.argv)
	program = program()
	sys.exit(App.exec())
