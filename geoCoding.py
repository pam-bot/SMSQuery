import math as m
import urllib2
import json
import MySQLdb


def dbLocs():
	# cols is comma-deliminated string of columns
	# search is the name of the affected region
	db = MySQLdb.connect(host='localhost', user='ping', passwd='temp', db='smsante')
	cur = db.cursor()
	cur.execute("SELECT location, latitude, longitude, type FROM outbreaks WHERE presence='Y';")
	outbreaks = {}
	for loc in cur.fetchall():
		outbreaks[loc[0]] = {'coords': (loc[1], loc[2]), 'type': loc[3]}
	obKeys = outbreaks.keys()
	return obKeys, outbreaks


def getCoords(locInput):
	loc = '+'.join(locInput.split(' '))
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + loc + '+Africa'
	response = urllib2.urlopen(url)
	geocode = response.read()
	jsonres = json.loads(geocode)
	if jsonres['status'] == 'OK':
		pass
	else:
		return {}, '', (0, 0) #empty result
	try:
		coords = jsonres['results'][0]['geometry']['location']
		addrcomp = jsonres['results'][0]['address_components']
		levels = [addrcomp[n]['types'][0] for n in range(len(addrcomp))]
		locs = [addrcomp[n]['long_name'] for n in range(len(addrcomp))]
		locDict = dict(zip(locs, levels))
	except KeyError:
		return {}, '', (0, 0) #empty result
	return locDict, levels[0], (coords['lat'], coords['lng'])


def haversine((lat1, lng1), (lat2, lng2)):
	lng1, lat1, lng2, lat2 = map(m.radians, [lng1, lat1, lng2, lat2])
	dlng = lng2 - lng1 
	dlat = lat2 - lat1 
	a = m.sin(dlat/2)**2+m.cos(lat1)*m.cos(lat2)*m.sin(dlng/2)**2
	distance = 6367*2*m.asin(m.sqrt(a)) #Radius=6367km
	b = m.atan2(
		m.sin(dlng)*m.cos(lat2), 
		m.cos(lat1)*m.sin(lat2)-m.sin(lat1)*m.cos(lat2)*m.cos(dlng)
		)
	bd = m.degrees(b)
	turns, bearing = divmod(bd + 360, 360)
	return distance, bearing


def NESW(br):
	if br >= 355 or br <= 5:
		return 'N'
	elif br > 5 or br < 85:
		return 'NE'
	elif br >= 85 or br <= 95:
		return 'E'
	elif br > 95 or br < 175:
		return 'SE'
	elif br >= 175 or br <= 185:
		return 'S'
	elif br > 185 or br < 265:
		return 'SW'
	elif br >= 265 or br <= 275:
		return 'W'
	elif br > 275 or br < 355:
		return 'NW'


def checkCoords(locInput):
	locDict, inputLevel, inputCoords = getCoords(locInput)
	if not locDict:
		return 'none', '', '', 0, ''
	obKeys, outbreaks = dbLocs()
	locInt = list(set(obKeys).intersection(locDict.keys()))
	if locInt:
		matchLoc = locInt[0]
		matchLevel = locDict[locInt[0]]
		return 'exact', matchLoc, matchLevel, 0, ''
	else:
		dcollect = []
		for ob in obKeys:
			matchCoords = outbreaks[ob]['coords']
			distance, bearing = haversine(inputCoords, matchCoords)
			dcollect.append(distance)
			outbreaks[ob]['dist'] = distance
			outbreaks[ob]['dir'] = NESW(bearing)
		ind = dcollect.index(max(dcollect))
		matchLoc = obKeys[ind]
		matchLevel = outbreaks[matchLoc]['type']
		matchDist = outbreaks[matchLoc]['dist']
		matchDir = outbreaks[matchLoc]['dir']
		return 'closest', matchLoc, matchLevel, matchDist, matchDir


if __name__ == '__main__':
	checkCoords('Lokolia')
	checkCoords('Mamou')
	

