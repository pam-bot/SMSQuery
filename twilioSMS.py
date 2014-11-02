from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
import geojson as gj

ACCOUNT_SID = "ACf10261d794fdaf920c6e1b08908cf198"
AUTH_TOKEN = "935387730b05191917e9773e8b03d0dd"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

#for message in client.messages.list():
	#print message.body

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	"""Respond to incoming calls with a simple text message."""
	from_number = request.values.get('From', None)
	from_body = request.values.get('Body', None)
	resp = twilio.twiml.Response()
	if from_number and from_body:
		resp.message(from_number+' '+from_body)
		return str(resp)
	else:
		return "Testing!"

if __name__ == "__main__":
	app.run(debug=True)

