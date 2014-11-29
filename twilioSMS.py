#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect
import twilio.twiml
from geoCoding import checkCoords


def processBody(body):
	body = ' '.join(body.split())
	usage = body.split(' ')[0]
	location = ' '.join(body.split(' ')[1:])
	defaultStr = u"S'il vous plaît excuser notre erreur. Taper 'infos' et le nom de votre ville et essayez à nouveau. Par example, 'infos Mamou'."
	regionDict = {u'locality': u'ville',
		u'administrative_area_level_2': u'région',
		u'administrative_area_level_1': u'province',
		u'country': u'pays'}
	if usage == 'infos':
		match, search, name, level, dist, nesw = checkCoords(location)
		if match == 'exact':
			sendStr = u"Vous avez cherché à {exactSearch}. Votre {exactLevel} {exactPlace} est sur notre liste des sites touchés par le virus Ebola.".format(exactLevel=regionDict[level], exactPlace=name, exactSearch=search)
		elif match == 'closest':
			sendStr = u"Vous avez cherché à {closeSearch}. Votre emplacement ne est pas sur notre liste des sites touchés par le virus Ebola. L'emplacement le plus proche est dans le {closeLevel} {closePlace} dans la direction {closeDir} à environ {closeDist:.0f} km".format(closeLevel=regionDict[level], closePlace=name, closeDist=dist, closeDir=nesw, closeSearch=search)
		elif match == 'none':
			sendStr = u"Vous avez cherché à {noneSearch}. ".format(noneSearch=search) + defaultStr
	else:
		sendStr = defaultStr
	return sendStr

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	"""twilioSMS for Ebola takes input text messages and connects 
	user requests to available outbreak information."""
	from_number = request.values.get('From', None)
	from_body = request.values.get('Body', None)
	sendStr = processBody(from_body)
	resp = twilio.twiml.Response()
	if from_number and from_body:
		resp.message(sendStr)
		return str(resp)
	else:
		return "Testing!"

if __name__ == "__main__":
	app.run(debug=True)

