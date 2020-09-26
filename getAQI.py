#Standards:
#	Naming
#	Commenting
#	Logging

# This is a program designed to webscrape the airnow.gov website, and find the current AQI data in eugene OR
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from Tools import *
from datetime import datetime
import os

# Used to get chromedriver from temp storage
def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.dirname(__file__)
	return os.path.join(base_path, relative_path)


def getAQI(url = "https://www.airnow.gov/?city=Eugene&state=OR&country=USA"):

	urlMOD = url.replace("%20", " ")

	CityI = 0
	StateI = 0
	AmperI = 0
	string = ""

	while string != "city=":
		string = urlMOD[CityI:CityI+5]
		CityI += 1
		if CityI > 100:
			break

	while string != "&":
		string = urlMOD[AmperI:AmperI+1]
		AmperI += 1
		if AmperI > 100:
			break

	City = urlMOD[CityI+4:AmperI-1]

	while string != "state=":
		string = urlMOD[StateI:StateI+6]
		StateI += 1
		if StateI > 100:
			break

	AmperI = AmperI + 5
	while string != "&":
		string = urlMOD[AmperI:AmperI+1]
		AmperI += 1
		if AmperI > 100:
			break

	State = urlMOD[StateI+5:AmperI-1]

	LoggerPrint("Getting AQI from: " + City + ", " + State , "Always")

	# Stuff to get chrome to work
	options = Options()  
	options.add_argument("--headless") 

	options.add_experimental_option('excludeSwitches', ['enable-logging'])

	# Starting chrome
	LoggerPrint("Initializing Chrome", "Information")
	LoggerPrint(str(resource_path('Chrome\\chromedriver.exe')),"Debug")
	browser = webdriver.Chrome(options=options, executable_path=resource_path('Chrome\\chromedriver.exe'))  
	LoggerPrint("Chrome Browser Initialized in Headless Mode", "Debug")

	# Get the url
	LoggerPrint("Getting url:  " + url, "Information")
	browser.get(url)

	# The delay in seconds
	delay = 3

	try:
		# Waits for three seconds. Don't ask me why, it just works.
		LoggerPrint("Waiting for webpage to load", "Information")
		myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'SHOULDNOTEXSIST')))
		LoggerPrint(" 'SHOULDNOTEXSIST', exists! The page may not be fully loaded!", "Warning")
	except TimeoutException:
		# Expected. IS NOT BAD. Just means it waited enough for the page to load.
		LoggerPrint("Loaded!", "Debug")

	# Save the inner html to a variable
	html = browser.page_source

	# Quitting chrome
	browser.quit()
	LoggerPrint("Browser Exited", "Information")

	# Takes the innerhtml, and saves it as text.
	html = html.encode('cp850','replace').decode('cp850')

	# Finds AQI
	i = html.find('<div class="aqi" data-tippy=""><b>')
	aqi = html[i+34:i+37]

	# Trims, if necessary
	if "<" in aqi:
		aqi = aqi[0:2]

	# Prints and returns
	LoggerPrint(aqi, "Debug")

	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	append_line("AQILog.txt", dt_string + "-->  " + aqi, folder="./Logs/")

	LoggerPrint("Got AQI", "Always")
	return int(aqi)

if __name__ == '__main__':
	print(getAQI(url="https://www.airnow.gov/?city=New%20Egypt&state=NJ&country=USA"))