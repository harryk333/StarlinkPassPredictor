# writeAcpPlan.py
#
# Take a list of events and write an ACP plan to observe them
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



# Writes an ACP observing script for the given events and imaging parameters
# observations array should be list of format [[name, date, RA, Dec]]
# Args: observations = array, exposure = num, repeat = num, filters = char, binning = num, imagepath = string, filename = string
# Returns: nothing
def writeAcpPlan(observations, Exposure=10, Repeat=1, Filters="v", Binning=1, imagePath = "E:\\data" , filename="plan.txt", shutdown=False):
	
	#Make a new file or overwrite an old one
	f = open(filename, "w")

	#Header to state when plan starts and ends
	f.write("; Start at %s\n" % (observations[0][1] - dt.timedelta(seconds = 300+480)).strftime('%Y/%m/%d %H:%M:%S'))
	f.write("; End at %s\n\n\n" % observations[-1][1].strftime('%Y/%m/%d %H:%M:%S'))


	#Default save path format
	f.write("#DIR " + imagePath + "\n\n\n")

	#Disable dithering
	f.write("#dither 0\n\n\n")


	#Autofocus
	#Wait until 5min before first sat to autofocus
	f.write("#WaitUntil 1, %s\n" % (observations[0][1] - dt.timedelta(seconds = 300)).strftime('%Y/%m/%d %H:%M:%S'))
	f.write("#autofocus\n")
	f.write("#nopreview\n")
	f.write("#count 1\n")
	f.write("#filter %s\n" % (Filters))
	f.write("#interval %s\n" % (Exposure))
	f.write("#binning %s\n" % (Binning))
	#Point the telescope somewhere reasonable
	f.write("#tag AltAz=%.5f,%.5f\n" % (90,75)) #az,alt
	#Target name, 0, 0 
	f.write("%s_\t0\t0\n\n\n" % ("autofocus"))


	#Add the instructions for each observation
	for obs in observations:

		name = obs[0]
		date = obs[1]
		offset = obs[2]
		RA = obs[3]
		Dec = obs[4]

		#Some comments for denoting the target
		f.write(";Sat %s at %s UT\n" % (name,date.strftime('%Y-%m-%d %H:%M:%S')))
		f.write(";----------------------------------------------------------------------------\n")

		#Wait until UTC time - 2min to start slewing
		f.write("#WaitUntil 1, %s\n" % (date - dt.timedelta(seconds = 90)).strftime('%Y/%m/%d %H:%M:%S'))

		#Don't preview images as they are captured
		f.write("#nopreview\n")
		#Take image because we have to
		f.write("#count 1\n")
		#Which filters to use, eg "r,i,z"
		f.write("#filter %s\n" % (Filters))
		#How long to expose for, eg "10,10,10"
		f.write("#interval %s\n" % (Exposure))
		#How many pixels to bin in a square pattern, eg "1,1,1"
		f.write("#binning %s\n" % (Binning))

		#Target name, RA, Dec 
		f.write("%s_Bkgd_\t%s\t%s\n\n" % (name, RA, Dec))
		

		f.write("#nopreview\n")
		#How many exposures to make of this target eg "1,1,1"
		f.write("#count %s\n" % (Repeat))
		#Which filters to use, eg "r,i,z"
		f.write("#filter %s\n" % (Filters))
		#How long to expose for, eg "10,10,10"
		f.write("#interval %s\n" % (Exposure))
		#How many pixels to bin in a square pattern, eg "1,1,1"
		f.write("#binning %s\n" % (Binning))

		#Wait until UTC time - offset to start
		f.write("#WaitUntil 1, %s\n" % (date - dt.timedelta(seconds = offset)).strftime('%Y/%m/%d %H:%M:%S'))
		
		#Target name, RA, Dec 
		f.write("%s_\t%s\t%s\n\n\n" % (name, RA, Dec))


	if shutdown:
		f.write("#shutdown\n")

	#Close the file for prosperity 
	f.close()




