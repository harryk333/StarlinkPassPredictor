# loadFile.py
#
# load TLE(s) from file
#
# Harry Krantz
# Steward Observatory
# University of Arizona
# May 2020


import requests
import pandas as pd




# Load TLE data from a local file
# Args: filename = path, satname = string
# Returns: array 
def loadFile(filename, satName="SATNAME"):
	#OPen the file 
	f = open(filename)

	#load the lines into an array
	content = f.read().splitlines()

	output = parseTLEFile(content, satName)

	return output




# Load TLE data from a web hosted file
# Args: filename = path, satname = string
# Returns: array
def loadFileURL(url, satName="SATNAME"):
	
	#Get stuff from the url
	f = requests.get(url)

	#load the lines into an array
	content = f.text.splitlines()

	output = parseTLEFile(content, satName)

	return output




# Parse a loaded file of TLE data
# Args: array of string, satname = string
# Returns: array
def parseTLEFile(stringList, satName="SATNAME"):

	output = []

	#Separate each TLE set
	lineNum = 0
	while lineNum < len(stringList):
		#If first line
		if stringList[lineNum][0:2] == "1 ":
			output.append([satName] + stringList[lineNum:lineNum+2])
			lineNum += 2
		#If second line
		elif stringList[lineNum][0:2] == "2 ":
			lineNum += 1
		#Else assum title line
		else:
			output.append(stringList[lineNum:lineNum+3])
			lineNum += 3


	return output




# Save data to a file
# Args: contents = array, filename = string
# Returns: nothing
def saveFile(contents, filename):
	#Make a new file or overwrite an old one
	f = open(filename, "w")

	for line in contents:
		try:
			f.write(line + "\n")
		except:
			for l in line:
				f.write(l + "\n")
	f.close()




# Save an array to a csv file with headers
# Args: filename = string, rows = array, headers = array
# Returns: nothing
def saveCSV(filename, rows, headers):
	df = pd.DataFrame(rows, columns=headers)
	df.to_csv(filename, index=None)



