#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'lib')
sys.path.insert(1, '')
from geoCoding import geoDate, checkCoords
import MySQLdb
import datetime

def geoResponse(body):
	lastUpdate = geoDate()
	location = '+'.join(body.split())
	defaultStr = u"S'il vous plaît excuser notre erreur. Taper le nom de votre ville et essayez à nouveau. Par example, 'Mamou'."
	regionDict = {u'locality': u'ville',
		u'administrative_area_level_2': u'région',
		u'administrative_area_level_1': u'province',
		u'country': u'pays'}
	match, search, name, level, dist, nesw = checkCoords(location)
	if match == 'exact':
		sendStr = u"Vous avez cherché à {exactSearch}. Votre {exactLevel} {exactPlace} est touchés par le virus Ebola. Dernière mise à jour: {lastUpdate}.".format(exactSearch=search, exactLevel=regionDict[level], exactPlace=name, lastUpdate=lastUpdate)
	elif match == 'closest':
		sendStr = u"Vous avez cherché à {closeSearch}. Ebola est détecté dans la {closeLevel} {closePlace} dans la direction {closeDir} à environ {closeDist:.0f} km. Dernière mise à jour: {lastUpdate}.".format(closeLevel=regionDict[level], closePlace=name, closeDist=dist, closeDir=nesw, closeSearch=search, lastUpdate=lastUpdate)
	elif match == 'none':
		sendStr = u"Vous avez cherché à {noneSearch}. ".format(noneSearch=body) + defaultStr
	elif match == 'over':
		sendStr = u"S'il vous plaît excuser notre erreur. Nous sommes sur notre limite d'utilisation pour aujourd'hui . Essayez à nouveau demain."
	else:
		sendStr = defaultStr
	return sendStr


def bedResponse():
	db = MySQLdb.connect(host='localhost', user='root', passwd='mysqltesting', db='sms_data')
	sql = "SELECT hospital_name,location,beds,last_update FROM hospital_beds;"
	with db:
		cur = db.cursor()
		cur.execute(sql)
		hospitals = cur.fetchall()
	sendStr = ''
	for hospital in hospitals:
		name = hospital[0]
		location = hospital[1]
		beds = hospital[2]
		last = hospital[3]
		newStr = u"L'hôpital {hospitalName} de {location} dispose de {beds} lits maintenant. Dernière mise à jour: {lastUpdate}. ".format(hospitalName=name, location=location, beds=beds, lastUpdate=last)
		sendStr = sendStr + newStr
	return sendStr


def logUser(from_number, from_body):
	db = MySQLdb.connect(host='localhost', user='root', passwd='mysqltesting', db='sms_input')
	sql = "INSERT INTO info_query (from_number,from_body) VALUES ('{0}','{1}');".format(from_number, from_body)
	with db:
		cur = db.cursor()
		cur.execute(sql)
	return


if __name__ == '__main__':
	print geoResponse('Lokolia')
	print geoResponse('Mamou')
	print geoResponse('Complete Nonsense')
