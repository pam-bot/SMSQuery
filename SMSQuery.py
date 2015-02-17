#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'lib')
sys.path.insert(1, '')

from flask import Flask, request, redirect
import twilio.twiml
from processInput import geoResponse, bedResponse

app = Flask(__name__)
app.config['DEBUG'] = True


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def SMSante():
	from_number = request.values.get('From', None)
	from_body = request.values.get('Body', None)
	resp = twilio.twiml.Response()
	if from_number and from_body:
		sendStr = geoResponse(from_body)
		resp.message(sendStr)
		return str(resp)
	else:
		from_number = '16135555555'
		from_body = 'Ottawa'
		return geoResponse(from_body)

if __name__ == "__main__":
	app.run(debug=True)


