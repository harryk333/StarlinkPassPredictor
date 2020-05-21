# main.py
# 
# This script utilizes the functions in the other files to calculate
# ephemerides for Starlink, determine which are visible, and create
# an ACP observing plan for the Pomenis telescope
#
# Harry Krantz
# Steward Observatory
# University of Arizona
# May 2020


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
#stop = dt.datetime.utcnow().replace(hour=7, minute=00, second=00)

#Restrict date range to morning or evening
start = dt.datetime(2020,5,21,0,00,00)
stop = dt.datetime(2020,5,21,7,00,00)

loc = locations["Lemmon"]

imagePath =  "E:\\data\\++__2020__++\\Sats\\%s_Starlink" % (start.strftime('%Y-%m-%d'))


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
passes = starlinkPassFinder(twilight, stop, loc, params, path)

#Select some to observe
passes = selectStarlinkPasses(passes, timePer, path)


###########################


#Make an ACP plan
filename = "starlinkPlan.txt"
print("Writing ACP Plan as " + filename)

#Reorganize for ACP plan
obs = []
for p in passes:
	obs.append([p["name"],p["maxTime"],offset,p["maxRA"],p["maxDec"],p["maxAlt"],p["maxAz"]])

#Write ACP plan for Pomenis
writeAcpPlan(obs, exposureTime, exposureRepeat, filterLetter, binning, imagePath, path + "/" + filename)


###########################


print("Done!")


