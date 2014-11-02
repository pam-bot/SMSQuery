from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
from Geocoding import checkLocation, checkLongitudeLatitude

#ACCOUNT_SID = "ACf10261d794fdaf920c6e1b08908cf198"
#AUTH_TOKEN = "935387730b05191917e9773e8b03d0dd"
#client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
#for message in client.messages.list():
	#print message.body

def processBody(body):
	usage = ' '.join(body.split()).split()[0].lower()
	location = ' '.join(body.split()).split()[1]
	if usage == 'check':
		coords, warn = checkLocation(location)
		dataList = [location] + coords
		if warn:
			sendStr = "Warning: Ebola has been confirmed at " + location
		else:
			sendStr = "No Ebola cases have been found at " + location
	elif usage == 'near':
		coords, distance = checkLongitudeLatitude(location)
		threshold = 100.0
		if distance < threshold:
			sendStr = "Warning: Ebola has been confirmed %.3f miles away" % distance
		else:
			sendStr = "No Ebola cases have been confirmed within " + str(threshold) + "miles"
	else:
		sendStr = "Please forgive our error. The input is invalid."
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

