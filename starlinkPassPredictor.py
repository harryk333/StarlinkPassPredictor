# starlinkPassPredictor.py
#
# pull the latest TLE's from Celestrak and computer valid observable passes
#
# Harry Krantz
# Steward Observatory
# University of Arizona
# May 2020


from findPass import *
from satFunctions import *
from loadFile import *




# Find all starlink passes for a given date range and location
# Args: start = datetime, stop = datetime, loc = skyfield Topos, path = string
# Returns: array of dict
def starlinkPassFinder(start, stop, loc, params = [False, None, False, 0], path=None):

	sunUp, moonUp, eclipsed, minAlt = params

	#Load the list of TLEs from a file
	print("Downloading TLE data from Celestrak...")
	url = "https://celestrak.com/NORAD/elements/supplemental/starlink.txt"
	tleList = loadFileURL(url)
	saveFile(tleList, path + "/starlinkTLE.txt")
	print("Downloaded " + str(len(tleList)) + " valid TLEs")

	print("Date Range: " + start.strftime('%Y-%m-%d %H:%M:%S') + " to " + stop.strftime('%Y-%m-%d %H:%M:%S'))

	print("Looking for observable satellites...\n")

	#Find all passes and filter them per paramters
	allPasses = []

	for tle in tleList:
		#Compute passes
		passes = findPass(tle, loc, start, stop)

		#Filter them for observable passes
		passes = filterPasses(passes, sunUp, moonUp, eclipsed, minAlt)
		
		allPasses += passes


	#Check that valid passes were found before continuing
	if len(allPasses) <= 0:
		print("Found " + str(len(allPasses)) + " observable passes" )
		exit()


	#Sort by time
	allPasses.sort(key=lambda p: p["maxTime"])


	print("\nFound " + str(len(allPasses)) + " observable passes" )
	print()
	printPassList(allPasses)
	print()


	if path != None:
		#Save list of observable passes to csv file
		saveCSV(path + "/" + "observablePasses.csv", makePassArray(allPasses), allPasses[0].keys())


	return allPasses




# select Starlink passes with time allowance inbetween
# Args: passes = array of dict, timePer = num, path = string
# Returns: array of dict
def selectStarlinkPasses(passes, timePer, path=None):

	#Sort by time
	passes.sort(key=lambda p: p["maxTime"])

	#Select passes for observation
	print("Selecting passes for observation...")
	selectPasses = [passes[0]]
	for p in passes:
		#if too soon since last observation skip this one
		if (p["maxTime"] - selectPasses[-1]["maxTime"]) < timePer:
			continue
		else:
			selectPasses.append(p)


	print("Selected " + str(len(selectPasses)) + " for observation")
	print()
	printPassList(selectPasses)
	print()


	if path != None:
		#Save list of selected passes to csv file
		saveCSV(path + "/" + "selectedPasses.csv", makePassArray(selectPasses), selectPasses[0].keys())


	return selectPasses





