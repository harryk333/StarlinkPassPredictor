# satFunctions.py
#
# Functions for computing satellite related things with Skyfield
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
import numpy as np

import skyfield.api


# Compute the ephemeris and other parameters for a given TLE, location, and singular time
# Args: tle = string, loc = skyfield topos, time = Skyfield Time or datetime
# Returns: dict
def computeEphemeris(tle, loc, time):

	#Split the tle
	name, line1, line2 = tle
	noradID = parseTLEID(tle)


	#Initialization of things
	sat = skyfield.sgp4lib.EarthSatellite(line1, line2, name)
	ts = skyfield.api.load.timescale()
	
	planets = skyfield.api.load('de421.bsp')
	earth = planets['earth']
	moon = planets['moon']
	sun = planets['sun']


	#Convert time if needed
	if type(time) == dt.datetime:
		time = ts.utc(time)


	#Compute satellite position
	geocentric = sat.at(time)
	subpoint = geocentric.subpoint()
	lat = subpoint.latitude
	lon = subpoint.longitude
	ele = subpoint.elevation

	difference = sat - loc
	topocentric = difference.at(time)
	alt, az, distance = topocentric.altaz()
	ra, dec, temp = topocentric.radec()


	#Angular velocity per second
	#Step time forward one second and get the difference in pointing	
	velocity = topocentric.separation_from( difference.at(ts.tt_jd(time.tt + 1/86400)) )

	
	#Skyfield does not have a built-in eclipsed function like PyEphem does :(
	#This is a crude way of doing it but should be fine for this purpose
	geocentricElong = geocentric.separation_from( earth.at(time).observe(sun) )
	geocentricDist = geocentric.distance()
	sunVectorSep = np.cos(geocentricElong.radians - np.pi/2) * geocentricDist.km
	earthRadius = 6378 #km
	umbraWidth = earthRadius - max(0, np.tan(np.radians(0.25)) * (np.sin(geocentricElong.radians - np.pi/2) * geocentricDist.km))
	eclipsed = sunVectorSep < umbraWidth
	

	#Determine if sun or moon is up and corresponging elongations
	l = (earth + loc).at(time)
	m = l.observe(moon).apparent()
	s = l.observe(sun).apparent()

	mAlt = m.altaz()[0]
	sAlt = s.altaz()[0]

	sunUp = sAlt.degrees > 0
	sunElong = topocentric.separation_from(s)

	moonUp = mAlt.degrees > 0
	moonElong = topocentric.separation_from(s)


	#Format output into dictionary
	passs = {
				"name" : name.strip(),
				"id" : noradID,
				"time" : time.utc_datetime(),
				"range" : distance.km,
				"height" : ele.km,
				"altitude" : alt.degrees,
				"azimuth" : az.degrees,
				"ra" : ra.hours,
				"dec" : dec.degrees,
				"lat" : lat.degrees,
				"lon" : lon.degrees,
				"velocity" : velocity.degrees,
				"sunElong" : sunElong.degrees,
				"moonElong" : moonElong.degrees,
				"eclipsed" : eclipsed,
				"sunUp" : sunUp,
				"moonUp" : moonUp
			}

	return passs




# Extract the epoch date from a TLE
# Args: tle = array of string
# Return: datetime 
def parseTLEdate(tle):
	year = int("20" + tle[1][18:20])
	day = float(tle[1][20:33])

	return dt.datetime(year-1,12,31,0,0,0) + dt.timedelta(day)




# Extract the NORAD ID from a TLE
# Args: tle = array pf string
# Returns: string
def parseTLEID(tle):
	return tle[1][2:8]




# Split TLE into the two/three lines
# Args: tle = array of string
# Returns: three strings
def splitTLE(tle):
	#Split on newline characters
	lines = tle.split("\n")

	#Actual TLE data should always be the last two lines
	line1 = lines[-2]
	line2 = lines[-1]

	#Check if there are three lines
	if len(lines) > 2:
		name = lines[0]
	else:
		name = "NONAME"

	return name, line1, line2




# Print the lines of a TLE
# Args: tle = array of string
# Returns: nothing
def printTLE(tle):
	for line in tle:
		print(line)




# Compute the checksum for a single TLE line
# Args: line = string
# Returns: num
def checksum(line):
	sum = 0
	for ch in line[:-1]:
		if ch.isdigit():
			sum += int(ch)
		if ch == "-":
			sum += 1
	return sum%10




# Compute and replace the checksum for a single TLE line
# Args: line = string
# Returns: string
def fixChecksum(line):
	return line[:-1] + str(checksum(line))



