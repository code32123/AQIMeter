import logging
import os
from datetime import datetime

showInformation = True
showDebug = True
silentMode = False

highest = 0

if not os.path.isdir("./Logs"):
	os.mkdir("./Logs")

for f in os.listdir("./Logs"):
	if not f == "AQILog.txt":
		number = int(f[3:4] if f[4:5] == "." else f[3:5])
		highest = highest if number < highest else number

def LoggerPrint(string, debugLevel):
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	prepend_line("Log" + str(highest + 1) + ".txt", dt_string + "-->  " + debugLevel + ":  " + string, folder="./Logs/")

	if not silentMode:
		if debugLevel == "Always":
			print(string)
		elif debugLevel == "Debug" and showDebug:
			print("DEBUG: " + string)
		elif debugLevel == "Warning" or debugLevel == "Warn":
			print("WARNING: " + string)
		elif (debugLevel == "Information" or debugLevel == "Info") and showInformation:
			print("INFO: " + string)
		elif (debugLevel == "CRITICAL" or debugLevel == "FATAL"):
			print("FATAL: " + string)
		else:
			LoggerPrint("Invalid Status for Print: " + string, "Warn")

#def prepend_line(file_name, line, folder="./"):
#	fullFile = folder + file_name
#	""" Insert given string as a new line at the beginning of a file """
#	if file_name in os.listdir(folder):
#		# define name of temporary dummy file
#		dummy_file = fullFile + '.bak'
#		# open original file in read mode and dummy file in write mode
#		with open(fullFile, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
#			# Write given line to the dummy file
#			write_obj.write(line + '\n')
#			# Read lines from original file one by one and append them to the dummy file
#			for line in read_obj:
#				write_obj.write(line)
#		# remove original file
#		os.remove(fullFile)
#		# Rename dummy file as the original file
#		os.rename(dummy_file, fullFile)
#	else:
#		with open(fullFile, "w+") as f:
#			f.write(line)
def prepend_line(file_name, line, folder="./"):
	fullFile = folder + file_name
	if file_name in os.listdir(folder):
		with open(fullFile, "a") as f:
			f.write("\n")
			f.write(line)	
	else:
		with open(fullFile, "w+") as f:
			f.write(line)