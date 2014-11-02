from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
from Geocoding import checkLocation, checkLongitudeLatitude
from unidecode import unidecode

#ACCOUNT_SID = "ACf10261d794fdaf920c6e1b08908cf198"
#AUTH_TOKEN = "935387730b05191917e9773e8b03d0dd"
#client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
#for message in client.messages.list():
	#print message.body

def processBody(body):
	usage = ' '.join(body.split()).split()[0].lower()
	location = ' '.join(body.split()).split()[1]
	if unidecode(usage) == 'verifier':
		coords, warn = checkLocation(location)
		if warn:
			sendStr = "Attention: Ebola a ete confirmer en " + location
		else:
			sendStr = "Ebola n'a pas ete confirmer en " + location
	elif unidecode(usage) == 'pres':
		distance = checkLongitudeLatitude(location)
		threshold = 1000.0
		if float(distance) < threshold:
			sendStr = "Attention: Ebola a ete confirmer vers " + distance + " km"
		else:
			sendStr = "Ebola n'a pas ete confirmer vers " + str(threshold) + " km"
	else:
		sendStr = "S'il vous plait excuser notre erreur. Votre entree est invalide."
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

