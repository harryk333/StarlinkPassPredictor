# locations.py
#
# a list of observatory locations
#
# Harry Krantz
# Steward Observatory
# University of Arizona
# May 2020


from skyfield.api import Topos




#empty dict
locations = {}

#Hopkins
hopkins = Topos(31.688, -110.883, elevation_m=2608)
locations["Hopkins"] = hopkins

#Bigelow
bigelow = Topos(32.4165, -110.7345, elevation_m=2510)
locations["Bigelow"] = bigelow

#Bok
bok = Topos(31.9629, -111.6004, elevation_m=2071)
locations["Bok"] = bok

#Lemmon
lemmon = Topos(32.44257, -110.7889, elevation_m=2805)
locations["Lemmon"] = lemmon
