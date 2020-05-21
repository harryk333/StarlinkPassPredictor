# writeAcpPlan.py
#
# take a list of events and write an ACP plan to observe them
#
# Harry Krantz
# Steward Observatory
# University of Arizona
# May 2020


import datetime as dt



# Writes an ACP observing script for the given events and imaging parameters
# observations array should be list of format [[name, date, RA, Dec]]
# Args: observations = array, exposure = num, repeat = num, filters = char, binning = num, imagepath = string, filename = string
# Returns: nothing
def writeAcpPlan(observations, Exposure=10, Repeat=1, Filters="v", Binning=1, imagePath = "E:\\data" , filename="plan.txt"):
	
	#Make a new file or overwrite an old one
	f = open(filename, "w")


	#Default save path format
	f.write("#DIR " + imagePath + "\n\n\n")


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
		f.write("#WaitUntil 1, %s\n" % (date - dt.timedelta(seconds = 120)).strftime('%Y/%m/%d %H:%M:%S'))

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



	#Close the file for prosperity 
	f.close()




