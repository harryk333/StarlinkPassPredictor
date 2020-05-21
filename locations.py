# locations.py
#
# A list of observatory locations
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
