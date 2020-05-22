# StarlinkPassPredictor
This is a collection of python code I wrote to calculate ephemerides for satellites from TLE data. Specifically this program is arranged to determine when to observe Starlink satellites. The base functions however can be used for any satellite TLE.

## Skyfield Dependence 
This program utilizes the Skyfield python library for all the behind the scenes astronomic calculations. Skyfield is an excellent astronomy library made by Brandon Rhodes who also made the popular PyEphem library; in some ways Skyfield is intended to replace and supersede PyEphem. 

Notably for calculating satellite positions Skyfield utilizes the proper SGP4 algorithms to match those used to generate a TLE and should the most accurate results.

[Skyfield Homepage](https://rhodesmill.org/skyfield/)

[Skyfield on GitHub](https://github.com/skyfielders/python-skyfield)

### Installing Skyfield
You can easily install Skyfield with pip

```
pip install skyfield
```

[See here for full instructions](https://rhodesmill.org/skyfield/installation.html)

### Additional Files
The first time you run the program Skyfield will automatically download several files to the working directory. These files are needed for Skyfield to make accurate calculations of astronomic bodies.

## Usage

The ```main.py``` file contains the script I use specifically for our telescope. You will likely not be able to use the same script but should use it as a template for creating your own. This script calls the functions from the other files to calculate the observable passes and then writes an ACP observing plan for our telescope. If your telescope can use ACP observing plans then you may find this script useful and will just need to adjust the timings and other parameters. 

```starlinkPassPredictor.py``` contains the main functional component for the overall program. This function downloads the latest TLE data for Starlink from Celestrak and then computes all observable passes for the given time range, location, and optional parameters. The optional parameters include whether or not the Sun or Moon is up, whether or not a satellite is eclisped by the Earth's shadow, and the minimum altitude above the horizon.

```satFunctions.py``` contains the function ```computeEphemeris()``` which is the encompassing function for calculating the exact position and other parameters for a satellite at a singular point in time.


### Incomplete Pass Error
When running the main pass predictor you may see an incomplete pass error in the console. This error is harmless and simply indicates that when calculating the next pass for the satellite it did not find a valid rise, peak, or set time within the given time range. This could be because the satellite was mid-pass during the start or end of the specified time window or the satellite will not rise or set as in the case of a GEO satellite.

The program ignores these errors and skips the satellite entirely.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
