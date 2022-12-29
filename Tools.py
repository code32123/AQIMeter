import logging
import os
from datetime import datetime

showInformation = True
showDebug = True
silentMode = False

highest = 0

# If it doesn't exist, create the logs folder
if not os.path.isdir("./Logs"):
	os.mkdir("./Logs")

# Find the highest number log file, excluding AQILog
for f in os.listdir("./Logs"):
	if not f == "AQILog.txt":
		number = int(f[3:4] if f[4:5] == "." else f[3:5])
		highest = highest if number < highest else number

# Logging mechanism, with debug levels, and logging to file.
def LoggerPrint(string, debugLevel="Invalid"):
	string = str(string)
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

	if not silentMode:
		if debugLevel == "Always":
			if showDebug:
				print("ALWAYS: " + string)
			else:
				print(string)
			debugLevel = "ALWAYS"
		elif debugLevel == "Debug" and showDebug:
			print("DEBUG: " + string)
			debugLevel = "DEBUG"
		elif debugLevel == "Warning" or debugLevel == "Warn":
			print("WARNING: " + string)
			debugLevel = "WARNING"
		elif (debugLevel == "Information" or debugLevel == "Info") and showInformation:
			print("INFO: " + string)
			debugLevel = "INFO"
		elif (debugLevel == "CRITICAL" or debugLevel == "FATAL"):
			print("FATAL: " + string)
			debugLevel = "FATAL"
		else:
			LoggerPrint("Invalid Status for Print: " + string, "Warn")
			debugLevel = "Invalid Status"

	append_line("Log" + str(highest + 1) + ".txt", dt_string + "-->  " + debugLevel + ":  " + string, folder="./Logs/")

# Appends a line to a file
def append_line(file_name, line, folder="./"):
	fullFile = folder + file_name
	if file_name in os.listdir(folder):
		with open(fullFile, "a") as f:
			f.write("\n")
			f.write(line)	
	else:
		with open(fullFile, "w+") as f:
			f.write(line)