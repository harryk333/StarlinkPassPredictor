# findPass.py
#
# Find all the observable passes of a satellite for a given location and time range
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


import datetime as dt

from satFunctions import *
from skyfield.api import utc




# Find all the valid flyover passes within the time frame for the provided TLE, location, and date range
# Args: tle = string, loc = skyfield topos, start = datetime, stop = datetime
# Returns: array of dict
def findPass(tle, loc, start, stop):

	#Split the tle
	name, line1, line2 = tle
	noradID = parseTLEID(tle)
	

	#Initialization
	sat = skyfield.sgp4lib.EarthSatellite(line1, line2, name)
	ts = skyfield.api.load.timescale()
	

	#Convert datetimes to Skyfield time objects
	try: 
		t0 = ts.utc(start)
		t1 = ts.utc(stop)
	except: #date lacks valid timezone, assuming utc
		t0 = ts.utc(start.replace(tzinfo=utc))
		t1 = ts.utc(stop.replace(tzinfo=utc))


	#Find flyover passes within time frame
	time, events = sat.find_events(loc, t0, t1, altitude_degrees = 0.0)

	
	#Construct passes from each set of three event types
	#Can definitley be done in a better more pythonic way
	passes = [] #list of type [ [rise,climax,set]... ]
	temp=[]
	for t, e in zip(time,events):
		temp.append(t)
		if e == 2:
			#Event type set, save the sublist and clear temp
			passes.append(temp)
			temp = []


	#Iterate through passes and compute ephemerides for each
	output = []
	for p in passes:
		try:
			rise = computeEphemeris(tle,loc,p[0])
			peak = computeEphemeris(tle,loc,p[1])
			sett = computeEphemeris(tle,loc,p[2])
		except IndexError as e:
			print("... incomplete pass, skipping!")
			continue

		#Determine pass duration
		try:
			duration = sett["time"] - rise["time"]
		except Exception as e: 
			print(e)
			duration = "error"


		#Organize parameters into dictionary for easy retrieval later
		passs = {
			"name" : rise["name"],
			"id" : rise["id"],
			"riseTime" : rise["time"],
			"riseAz" : rise["azimuth"],
			"maxTime" : peak["time"],
			"maxAlt" : peak["altitude"],
			"maxAz" : peak["azimuth"],
			"maxRA" : peak["ra"],
			"maxDec" : peak["dec"],
			"maxVel" : peak["velocity"],
			"range" : peak["range"],
			"height" : peak["height"],
			"sunElong" : peak["sunElong"],
			"moonElong" : peak["moonElong"],
			"setTime" : sett["time"],
			"setAz" : sett["azimuth"],
			"duration" : duration,
			"eclipsed" : peak["eclipsed"],
			"sunUp" : peak["sunUp"],
			"moonUp" : peak["moonUp"]
		}

		#Save the parameters
		output.append(passs)

	return output




# Filter a list of passes for certain conditions
# None is a wildcard
# Args: passes = array of dict, sun = bool, moon = bool, eclipsed = bool, alt=num
# Returns: array of dict
def filterPasses(passes, sun=None, moon=None, eclipsed=None, alt=None):
	output = []

	for p in passes:
		#Check for invalidations
		if  (sun != None and p["sunUp"] != sun):
			continue
		if (moon != None and p["moonUp"] != moon):
			continue
		if (eclipsed != None and p["eclipsed"] != eclipsed):
			continue
		if (alt != None and p["maxAlt"] < alt):
			continue

		#If valid, append pass to output list
		output.append(p)

	return output




# Prints the info from a single pass event in the format: [name, id, riseTime, riseAz, maxAltTime, maxAlt, maxAz, setTime, setAz, duration, eclipsed, sunUp, moonUp]
# Args: passs = dict
# Returns: nothing
def printPass(passs):
	print("{: <24} {: <8} {: <21} {: <14.7s} {: <21} {: <10.7s} {: <14.7s} {: <21} {: <13.7s} {: <13.7s}".format(*map(str, [passs["name"], passs["id"], passs["riseTime"].strftime('%Y-%m-%d %H:%M:%S'), passs["riseAz"], passs["maxTime"].strftime('%Y-%m-%d %H:%M:%S'), passs["maxAlt"], passs["maxAz"], passs["setTime"].strftime('%Y-%m-%d %H:%M:%S'), passs["setAz"], passs["duration"]])))




# Prints a full list of pass events with informative header
# Args: passes = array of dict
# Returns: nothing
def printPassList(passes):
	#Print the header and list of passes
	headers = ["Name", "ID", "Rise Time", "Rise Azimuth", "Peak Time", "Peak Alt", "Peak Azimuth", "Set Time", "Set Azimuth", "Duration"]
	print("{: <24} {: <8} {: <21} {: <14} {: <21} {: <10} {: <14} {: <21} {: <13} {: <13}".format(*headers))
	print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
	for p in passes:
		printPass(p)




# Reformat array of dicts into singular array with the requested values in headerNames
# Args: passes = array of dict, headerNames = array of string
# Returns: array
def makePassArray(passes, headerNames=None):
	if headerNames == None:
		headerNames = passes[0].keys()
	output = []
	for p in passes:
		output.append( [ p[h] for h in headerNames ] )
	return output 



