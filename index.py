#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# SDK notes
cd $HOME/Install/google_appengine
ROOT=$HOME/Dropbox/Repos/SMSante
python dev_appserver.py $ROOT
#python appcfg.py -A emerald-pipe-781 --oauth2 update $ROOT
"""

import sys
sys.path.insert(0, 'lib')
sys.path.insert(1, '')

from flask import Flask, request, jsonify, render_template
import twilio.twiml
import MySQLdb

# functions of script:
# - take SMS input
# - store metadata into input database
# - pass query id and message body to javascript

def store_query(number, body):
	db = MySQLdb.connect(host='localhost', user='root', passwd='mysqltesting', db='sms_input')
	sql_command = """INSERT INTO info_query (from_number,from_body) 
		VALUES ('{0}','{1}');""".format(number, body)
	with db:
		cur = db.cursor()
		cur.execute(sql_command)
		qid = cur.lastrowid
	return qid


app = Flask(__name__)
app.config['DEBUG'] = True


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def SMSante():
	from_number = request.values.get('From', None)
	from_body = request.values.get('Body', None)
	if from_number and from_body:
		qid = store_query(from_number, from_body)
		return render_template('middle.html', input_data=(qid, from_body))
	else:
		# just for tests
		# otherwise send back that data wasn't received
		# resp = twilio.twiml.Response()
		# resp.message('Message not received.')
		from_number = '+16135555555'
		from_body = 'Ottawa'
		qid = store_query(from_number, from_body)
		return render_template('middle.html', input_data=(qid, from_body))


@app.route('/geocode')
def add_numbers():
    lat = request.args.get('lat', 0, type=float)
    lng = request.args.get('lng', 0, type=float)
    return jsonify(result="Got coords = ("+str(lat)+", "+str(lng)+")")


if __name__ == '__main__':
	app.run(debug=True)


"""
env = os.getenv('SERVER_SOFTWARE')
if (env and env.startswith('Google App Engine/')):
	db = MySQLdb.connect(unix_socket='/cloudsql/emerald-pipe-781:testsql', user='root', db='testdb')
	cur = db.cursor()
	cur.execute("SELECT nationality FROM people WHERE name='Pam';")
	result = cur.fetchone()
else:
	db = MySQLdb.connect(host='173.194.85.163', port=3306, user='root', passwd='testpassword', db='testdb')
	cur = db.cursor()
	cur.execute("SELECT nationality FROM people WHERE name='Pam';")
	result = cur.fetchone()
"""
