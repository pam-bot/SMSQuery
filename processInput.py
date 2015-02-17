#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'lib')
sys.path.insert(1, '')
from geoCoding import checkCoords


def geoResponse(body):
	location = '+'.join(body.split())
	defaultStr = u"S'il vous plaît excuser notre erreur. Taper le nom de votre ville et essayez à nouveau. Par example, 'Mamou'."
	regionDict = {u'locality': u'ville',
		u'administrative_area_level_2': u'région',
		u'administrative_area_level_1': u'province',
		u'country': u'pays'}
	match, search, name, level, dist, nesw = checkCoords(location)
	if match == 'exact':
		sendStr = u"Vous avez cherché à {exactSearch}. Votre {exactLevel} {exactPlace} est touchés par le virus Ebola.".format(exactLevel=regionDict[level], exactPlace=name, exactSearch=search)
	elif match == 'closest':
		sendStr = u"Vous avez cherché à {closeSearch}. Ebola est détecté dans la {closeLevel} {closePlace} dans la direction {closeDir} à environ {closeDist:.0f} km".format(closeLevel=regionDict[level], closePlace=name, closeDist=dist, closeDir=nesw, closeSearch=search)
	elif match == 'none':
		sendStr = u"Vous avez cherché à {noneSearch}. ".format(noneSearch=body) + defaultStr
	elif match == 'over':
		sendStr = u"S'il vous plaît excuser notre erreur. Nous sommes sur notre limite d'utilisation pour aujourd'hui . Essayez à nouveau demain."
	else:
		sendStr = defaultStr
	return sendStr


def bedResponse():
	return


if __name__ == '__main__':
	print geoResponse('Lokolia')
	print geoResponse('Mamou')
	print geoResponse('Complete Nonsense')
