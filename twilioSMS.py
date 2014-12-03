#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'lib')
sys.path.insert(1, '')

from flask import Flask, request, redirect
import twilio.twiml
from geoCoding import checkCoords

app = Flask(__name__)
app.config['DEBUG'] = True

def processBody(body):
	body = ' '.join(body.split())
	usage = body.split(' ')[0].lower()
	location = ' '.join(body.split(' ')[1:])
	defaultStr = u"S'il vous plaît excuser notre erreur. Taper 'infos' et le nom de votre ville et essayez à nouveau. Par example, 'infos Mamou'."
	regionDict = {u'locality': u'ville',
		u'administrative_area_level_2': u'région',
		u'administrative_area_level_1': u'province',
		u'country': u'pays'}
	if 'infos' in usage:
		match, search, name, level, dist, nesw = checkCoords(location)
		if match == 'exact':
			sendStr = u"Vous avez cherché à {exactSearch}. Votre {exactLevel} {exactPlace} est sur notre liste des sites touchés par le virus Ebola.".format(exactLevel=regionDict[level], exactPlace=name, exactSearch=search)
		elif match == 'closest':
			sendStr = u"Vous avez cherché à {closeSearch}. La location avec Ebola le plus proche est dans le {closeLevel} {closePlace} dans la direction {closeDir} à environ {closeDist:.0f} km".format(closeLevel=regionDict[level], closePlace=name, closeDist=dist, closeDir=nesw, closeSearch=search)
		elif match == 'none':
			sendStr = u"Vous avez cherché à {noneSearch}. ".format(noneSearch=search) + defaultStr
	else:
		sendStr = defaultStr
	return sendStr

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def SMSante():
	from_number = request.values.get('From', None)
	from_body = request.values.get('Body', None)
	resp = twilio.twiml.Response()
	if from_number and from_body:
		sendStr = processBody(from_body)
		resp.message(sendStr)
		return str(resp)
	else:
		return 'If you can read this, everything is working.'

#if __name__ == "__main__":
	#app.run(debug=True)

