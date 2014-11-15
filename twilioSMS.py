from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
from Geocoding import checkLocation, checkLongitudeLatitude
from unidecode import unidecode
 # -*- coding: iso-8859-1 -*-

def processBody(body):
	usage = ' '.join(body.split()).split()[0].lower()
	location = ' '.join(body.split()).split()[1]
	if unidecode(usage) == 'verifier':
		coords, warn = checkLocation(location)
		if warn:
			sendStr = u"Attention: Ebola a été confirmer en " + location
		else:
			sendStr = u"Ebola n'a pas été confirmer en " + location
	elif unidecode(usage) == 'pres':
		distance = checkLongitudeLatitude(location)
		threshold = 1000.0
		if float(distance) < threshold:
			sendStr = u"Attention: Ebola a été confirmer vers " + distance + " km"
		else:
			sendStr = u"Ebola n'a pas été confirmer vers " + str(threshold) + " km"
	else:
		sendStr = u"S'il vous plaît excuser notre erreur. Votre entrée est invalide."
	return sendStr 

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	"""twilioSMS for Ebola takes input text messages
	and connects user requests (i.e. loc) to available
	outbreak information."""
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
