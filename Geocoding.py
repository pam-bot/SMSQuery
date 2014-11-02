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
	latitude1 = jsonformatted['results'][0]["geometry"]["viewport"]["northeast"]["lat"]
	latitude2 = jsonformatted['results'][0]["geometry"]["viewport"]["southwest"]["lat"]
	longitude1 = jsonformatted['results'][0]["geometry"]["viewport"]["northeast"]["lng"]
	longitude2 = jsonformatted['results'][0]["geometry"]["viewport"]["southwest"]["lng"]
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
	coords = [latitude, longitude]
	threshold = 100.0
	Distances = []
	for k in range(2,len(outbreak_data["features"])):
		if "coordinates" in outbreak_data["features"][k]["geometry"]:
			targetlatitude = outbreak_data["features"][k]["geometry"]["coordinates"][0]*math.pi/180
			targetlongitude = outbreak_data["features"][k]["geometry"]["coordinates"][1]*math.pi/180
			dlat=math.fabs(latitude-targetlatitude)
			dlon=math.fabs(longitude-targetlongitude)
			Rm = 3961
			a = Decimal(math.pow(math.sin(dlat/2),2) + math.cos(latitude) * math.cos(targetlatitude) * math.pow(math.sin(dlon/2),2))
			Distances.append(Decimal(2 * math.atan2(math.sqrt(a), math.sqrt(1-a))))
	HaversineDistance = min(Distances)
	if HaversineDistance < threshold:
		return coords, HaversineDistance
	else:
		return [], threshold


def runGeocoding(location):
	location, latitude, longitude, outbreak_data = loadData(location)
	coords1, result = checkLocation(location)
	coords2, distance = checkLongitudeLatitude(location)
	print coords1, result, coords2, distance

if __name__ == "__main__":
	runGeocoding("Lokolia")

