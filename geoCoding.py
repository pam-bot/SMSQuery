#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'lib')

import os
import math as m
import urllib2
import json
import MySQLdb


def dbLocs():
	db = MySQLdb.connect(host='localhost', user='root', passwd='mysqltesting', db='sms_data')
	sql_cmd = """SELECT * FROM outbreaks WHERE presence='Y';"""
	with db:
		cur = db.cursor()
		cur.execute(sql_cmd)
		data = cur.fetchall()
	outbreaks = {}
	for loc in data:
		outbreaks[loc[0]] = {'coords': (loc[1], loc[2]), 'type': loc[3]}
	obKeys = outbreaks.keys()
	return obKeys, outbreaks


def getCoords(locInput):
	loc = '+'.join(locInput.split(' '))
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + loc + '+Africa'
	response = urllib2.urlopen(url)
	geocode = response.read()
	jsonres = json.loads(geocode)
	emptyResult = unicode(locInput), {}, '', (0, 0)
	if jsonres['status'] == 'OK':
		pass
	else:
		return emptyResult
	try:
		coords = jsonres['results'][0]['geometry']['location']
		addrcomp = jsonres['results'][0]['address_components']
		levels = [addrcomp[n]['types'][0] for n in range(len(addrcomp))]
		locs = [addrcomp[n]['long_name'] for n in range(len(addrcomp))]
		locDict = dict(zip(locs, levels))
		searchRes = addrcomp[0]['long_name']
	except KeyError:
		return emptyResult
	return searchRes, locDict, levels[0], (coords['lat'], coords['lng'])


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
	elif br > 5 and br < 85:
		return 'NE'
	elif br >= 85 and br <= 95:
		return 'E'
	elif br > 95 and br < 175:
		return 'SE'
	elif br >= 175 and br <= 185:
		return 'S'
	elif br > 185 and br < 265:
		return 'SW'
	elif br >= 265 and br <= 275:
		return 'W'
	elif br > 275 and br < 355:
		return 'NW'


def checkCoords(locInput):
	searchRes, locDict, inputLevel, inputCoords = getCoords(locInput)
	if not locDict:
		return 'none', searchRes, '', '', 0, ''
	obKeys, outbreaks = dbLocs()
	locInt = list(set(obKeys).intersection(locDict.keys()))
	if locInt:
		matchLoc = locInt[0]
		matchLevel = locDict[locInt[0]]
		return 'exact', searchRes, matchLoc, matchLevel, 0, ''
	else:
		dcollect = []
		for ob in obKeys:
			matchCoords = outbreaks[ob]['coords']
			distance, bearing = haversine(inputCoords, matchCoords)
			dcollect.append(distance)
			outbreaks[ob]['dist'] = distance
			outbreaks[ob]['dir'] = NESW(bearing)
		ind = dcollect.index(min(dcollect))
		matchLoc = unicode(obKeys[ind])
		matchLevel = unicode(outbreaks[matchLoc]['type'])
		matchDist = outbreaks[matchLoc]['dist']
		matchDir = outbreaks[matchLoc]['dir']
		return 'closest', searchRes, matchLoc, matchLevel, matchDist, matchDir


if __name__ == '__main__':
	print checkCoords('Lokolia')
	print checkCoords('Mamou')
	print checkCoords('Complete Nonsense')
	

