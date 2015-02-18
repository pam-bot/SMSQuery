#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'lib')
sys.path.insert(1, '')

from flask import Flask, request, redirect
import twilio.twiml
from processInput import geoResponse, bedResponse, logUser

app = Flask(__name__)
app.config['DEBUG'] = True


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def SMSante():
	from_number = request.values.get('From', None)
	from_body = request.values.get('Body', None)
	resp = twilio.twiml.Response()
	if from_number and from_body:
		geoStr = geoResponse(from_body)
		bedStr = bedResponse()
		resp.message(geoStr + ' ' + bedStr)
		logUser(from_number, from_body)
		return str(resp)
	else:
		from_number = '16135555555'
		from_body = 'Ottawa'
		geoStr = geoResponse(from_body)
		bedStr = bedResponse()
		return geoStr + ' ' + bedStr

if __name__ == "__main__":
	app.run(debug=True)


