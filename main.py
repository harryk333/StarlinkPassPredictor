# main.py
# 
# This script utilizes the functions in the other files to calculate
# ephemerides for Starlink, determine which are visible, and create
# an ACP observing plan for the Pomenis telescope
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
import os

from starlinkPassPredictor import *
from locations import locations
from writeAcpPlan import *

from skyfield import api
from skyfield import almanac




##########################
#  Parameters
##########################

exposureTime = 3
exposureRepeat = 1
filterLetter = "v"
binning = 1

offset = 9 #offset the requested time to allow for slewing etc. 6 sec for starting at center of FOV. increase to trigger sooner
timePer = dt.timedelta(seconds=120) #minimum number of sec to wait before next target

minAlt = 20
sunUp = False
moonUp = None #any
eclipsed = False

params = [sunUp, moonUp, eclipsed, minAlt]

#start = dt.datetime.utcnow().replace(hour=0, minute=00, second=00)
#stop = dt.datetime.utcnow().replace(hour=5, minute=00, second=00)

start = dt.datetime(2020,5,28,0,00,00)
stop = dt.datetime(2020,5,28,5,00,00)

loc = locations["Lemmon"]

imagePath =  "F:\\++__2020.5__++\\Sats\\%s_Starlink" % (start.strftime('%Y-%m-%d'))


###########################


#Make a new directory for todays data
path = start.strftime('%Y-%m-%d')

if os.path.isdir(path):
	print("%s already exists, opening it..." % path)
else:
	try:
	    os.mkdir(path)
	except OSError:
	    print ("Creation of the directory %s failed" % path)
	else:
	    print ("Successfully created the directory %s " % path)


###########################


ts = api.load.timescale()
e = api.load('de421.bsp')


### Evening ###
print("\n\n ### EVENING ### \n\n")


#Determine when is sunset and twilight
t, y = almanac.find_discrete(ts.utc(start.replace(tzinfo=api.utc)), ts.utc(stop.replace(tzinfo=api.utc)), almanac.dark_twilight_day(e, loc))

for ti, yi in zip(t,y):
	if yi == 3:
		sunset = ti
	if yi == 1:
		twilight = ti

twilight = twilight.utc_datetime()

print("Astronomical Twilght is " + twilight.strftime('%Y-%m-%d %H:%M:%S') )


###########################


#Find all passes
passes = starlinkPassPredictor(twilight, stop, loc, params, path, "selectedPassesEvening")
# passes = starlinkPassPredictor(start, twilight, loc, params, path)


#Select some to observe
passes = selectStarlinkPasses(passes, timePer, path, "selectedPassesEvening")


###########################


#Make an ACP plan
filename = "starlinkPlanEvening.txt"
print("Writing ACP Plan as " + filename)

#Reorganize for ACP plan
obs = []
for p in passes:
	obs.append([p["name"],p["maxTime"],offset,p["maxRA"],p["maxDec"],p["maxAlt"],p["maxAz"]])

#Write ACP plan for Pomenis
writeAcpPlan(obs, exposureTime, exposureRepeat, filterLetter, binning, imagePath, path + "/" + filename)



### Morning ###

print("\n\n ### MORNING ### \n\n")

#start = dt.datetime.utcnow().replace(hour=9, minute=00, second=00)
#stop = dt.datetime.utcnow().replace(hour=15, minute=00, second=00)

start = dt.datetime(2020,5,28,9,00,00)
stop = dt.datetime(2020,5,28,15,00,00)


#Determine when is sunset and twilight
t, y = almanac.find_discrete(ts.utc(start.replace(tzinfo=api.utc)), ts.utc(stop.replace(tzinfo=api.utc)), almanac.dark_twilight_day(e, loc))

for ti, yi in zip(t,y):
	if yi == 3:
		sunset = ti
	if yi == 1:
		twilight = ti

twilight = twilight.utc_datetime()

print("Astronomical Twilght is " + twilight.strftime('%Y-%m-%d %H:%M:%S') )


###########################


#Find all passes
passes = starlinkPassPredictor(start, twilight, loc, params, path, "selectedPassesMorning")

#Select some to observe
passes = selectStarlinkPasses(passes, timePer, path, "selectedPassesMorning")


###########################


#Make an ACP plan
filename = "starlinkPlanMorning.txt"
print("Writing ACP Plan as " + filename)

#Reorganize for ACP plan
obs = []
for p in passes:
	obs.append([p["name"],p["maxTime"],offset,p["maxRA"],p["maxDec"],p["maxAlt"],p["maxAz"]])

#Write ACP plan for Pomenis
writeAcpPlan(obs, exposureTime, exposureRepeat, filterLetter, binning, imagePath, path + "/" + filename)


###########################


print("Done!")



