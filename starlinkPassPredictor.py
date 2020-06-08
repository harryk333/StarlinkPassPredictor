# starlinkPassPredictor.py
#
# Pull the latest Starlink TLEs from Celestrak and find observable passes
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


import os

from findPass import *
from satFunctions import *
from loadFile import *




# Find all starlink passes for a given date range and location
# Args: start = datetime, stop = datetime, loc = skyfield Topos, path = string
# Returns: array of dict
def starlinkPassPredictor(start, stop, loc, params = [False, None, False, 0], path=None, filename="observablePasses"):

	sunUp, moonUp, eclipsed, minAlt = params

	#Load the list of TLEs from a file
	print("Downloading TLE data from Celestrak...")
	url = "https://celestrak.com/NORAD/elements/supplemental/starlink.txt"
	tleList = loadFileURL(url)
	saveFile(tleList, os.path.join(path, "starlinkTLE.txt"))
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
		saveCSV( os.path.join(path, filename + ".csv"), makePassArray(allPasses), allPasses[0].keys())


	return allPasses




# select Starlink passes with time allowance inbetween
# Args: passes = array of dict, timePer = num, path = string
# Returns: array of dict
def selectStarlinkPasses(passes, timePer, path=None, filename="selectedPasses"):

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
		saveCSV( os.path.join(path, filename + ".csv"), makePassArray(selectPasses), selectPasses[0].keys())


	return selectPasses





