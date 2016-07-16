import json
import urllib2

address="Monrovia"
url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&components=country:LR" % address

response = urllib2.urlopen(url)
jsongeocode = response.read()
print jsongeocode