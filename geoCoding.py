import sys
import json
import urllib2
import math
from decimal import *

"""
def loadData(location):
	location, latitude, longitude = getCoords(location)
	# Open outbreak data
	with open('locations.geojson') as json_file:
		outbreak_data = json.load(json_file)
	return location, latitude, longitude, outbreak_data

   
# Pre-check for town's presence in outbreak
def checkLocation(location):
	location, latitude, longitude, outbreak_data = loadData(location)
	for i in range(2,len(outbreak_data['features'])):
		if 'address' in outbreak_data['features'][i]['properties']:
			if location == outbreak_data['features'][i]['properties']['address']:
				coords = outbreak_data['features'][i]['geometry']['coordinates']
				return coords, 'warn'
	else:
		return [], ''


# Scan Latitudes and Longitudes for outbreaks within a mile, using the Haversine Function. 
def checkLongitudeLatitude(location):
	location, latitude, longitude, outbreak_data = loadData(location)
	towns = [outbreak_data['features'][k]['properties']['address'] for k in range(2, len(outbreak_data['features'])) if 'address' in outbreak_data['features'][k]['properties']]
	alldist = []
	for name in towns:
		if ' ' in name:
			continue 
		elif 'York' in name:
			continue
		url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+location+'+Africa&destinations='+name+'+Africa'
		response = urllib2.urlopen(url)
		rjson = response.read()
		fjson = json.loads(rjson)
		try:
			dist = float(fjson['rows'][0]['elements'][0]['distance']['value'])
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
"""

import urllib2
import json
import MySQLdb

"""
Ideas:
- user inputs text, goes through Google check
- corrected input is checked with DB for presence of outbreak
	- also see if within subregion of DB entry
- if not,
- each DB location scanned for haversine with input
- output smallest distance 
"""


def dbSelect(search):
	db = MySQLdb.connect(host='localhost', user='ping', passwd='temp', db='smsante')
	cur = db.cursor() 
	cur.execute("SELECT * FROM outbreaks WHERE location='" + search + 
		"' AND presence='Y';")
	results = []
	for row in cur.fetchall():
		results.append(row)
	return results


def getCoords(location):
	loc = '+'.join(location.split(' '))
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + loc
	response = urllib2.urlopen(url)
	geocode = response.read()
	jsonres = json.loads(geocode)
	if jsonres['status'] == 'OK':
		pass
	else: # add elifs
		print 'Error. Status not okay'
	coords = jsonres['results'][0]['geometry']['location']
	# just to make sure match is correct, delete later
	locmatch = jsonres['results'][0]['address_components'][0]['long_name']
	# later: accomodate levels of geography (is something within something)
	# ['locality', 'administrative_area_level_2',
	# 'administrative_area_level_1', 'country']
	return locmatch, coords['lat'], coords['lng']


if __name__ == '__main__':
	location = ' '.join(sys.argv[1:])
	loc, lat, lng = getCoords(location)
	print '%s\t%f\t%f' %(loc, lat, lng)

