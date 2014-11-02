import json
import urllib2
import math
from decimal import *


def loadData(location):
	location, latitude, longitude = getCoords(location)
	# Open outbreak data
	with open("locations.geojson") as json_file:
		outbreak_data = json.load(json_file)
	return location, latitude, longitude, outbreak_data


def getCoords(location):
	location = location
	url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&components=country:LR" % location
	# Pull data from Google Maps API
	response = urllib2.urlopen(url)
	jsongeocode = response.read()
	# Format the data as a JSON object
	jsonformatted = json.loads(jsongeocode)
	# Pull Latitude and Longitude Data
	latitude1 = jsonformatted['results'][0]["geometry"]["viewport"]["northeast"]["lat"]*math.pi/180
	latitude2 = jsonformatted['results'][0]["geometry"]["viewport"]["southwest"]["lat"]*math.pi/180
	longitude1 = jsonformatted['results'][0]["geometry"]["viewport"]["northeast"]["lng"]*math.pi/180
	longitude2 = jsonformatted['results'][0]["geometry"]["viewport"]["southwest"]["lng"]*math.pi/180
	# Average the Northeastern and Southwestern Data for an average coordinate
	return location, (latitude1+latitude2)/2, (longitude1+longitude2)/2

   
# Pre-check for town's presence in outbreak
def checkLocation(location):
	location, latitude, longitude, outbreak_data = loadData(location)
	for i in range(2,len(outbreak_data["features"])):
		if "address" in outbreak_data["features"][i]["properties"]:
			if location == outbreak_data["features"][i]["properties"]["address"]:
				coords = outbreak_data["features"][i]["geometry"]["coordinates"]
				return coords, "warn"
	else:
		return [], ""


# Scan Latitudes and Longitudes for outbreaks within a mile, using the Haversine Function. 
def checkLongitudeLatitude(location):
	location, latitude, longitude, outbreak_data = loadData(location)
	towns = [outbreak_data["features"][k]["properties"]["address"] for k in range(2, len(outbreak_data["features"])) if "address" in outbreak_data["features"][k]["properties"]]
	alldist = []
	for name in towns:
		if " " in name:
			continue 
		elif "York" in name:
			continue
		url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+location+"+Africa&destinations="+name+"+Africa"
		response = urllib2.urlopen(url)
		rjson = response.read()
		fjson = json.loads(rjson)
		try:
			dist = float(fjson["rows"][0]["elements"][0]["distance"]["value"])
		except KeyError:
			continue
		alldist.append(dist)
	udist = min(alldist)
	return str(udist/1000.0)


def runGeocoding(location):
	location, latitude, longitude, outbreak_data = loadData(location)
	coords1, result = checkLocation(location)
	distance = checkLongitudeLatitude(location)
	print coords1, result, distance

if __name__ == "__main__":
	runGeocoding("Mamou")

