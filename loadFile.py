# loadFile.py
#
# Load TLE(s) from file or save calculated data
#
# Harry Krantz
# Steward Observatory
# University of Arizona
# Copyright May 2020
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


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



