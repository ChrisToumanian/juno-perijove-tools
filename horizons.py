#! /usr/local/bin/python

import sys
import urllib.request
import math
from datetime import datetime, timedelta

def get_julian_datetime(date):
	# Ensure correct format
	if not isinstance(date, datetime):
		raise TypeError('Invalid type for parameter "date" - expecting datetime')
	elif date.year < 1801 or date.year > 2099:
		raise ValueError('Datetime must be between year 1801 and 2099')

	# Perform the calculation
	julian_datetime = 367 * date.year - int((7 * (date.year + int((date.month + 9) 
	/ 12.0))) / 4.0) + int((275 * date.month) / 9.0) + date.day + 1721013.5 
	+ (date.hour + date.minute / 60.0 + date.second / math.pow(60,2)) / 24.0 
	- 0.5 * math.copysign(1, 100 * date.year + date.month - 190002.5) + 0.5

	return julian_datetime

class HorizonsRequest:
	def __init__(self, center, target, datetime, quantities):
		self.keys = {
			"CENTER": center,
			"COMMAND": target,
			"QUANTITIES": quantities,
			"TLIST": str(get_julian_datetime(datetime)),
			"MAKE_EPHEM": "YES",
			"OBJ_DATA": "NO",
			"TABLE_TYPE": "OBSERVER",
			"CAL_FORMAT": "BOTH",
			"ANG_FORMAT": "DEG",
			"CSV_FORMAT": "YES"
		}
		self.response = []
		self.dictionary = {}
	
	def set_key(self, key, value):
		self.keys[key] = str(value)

	def delete_key(self, key):
		self.keys.pop(key, None)	

	def send(self):
		# create request
		request = "https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1"
		for key in self.keys:
			request += "&" + key + "='" + self.keys[key] + "'"

		# send request
		file = urllib.request.urlopen(request)
		for line in file:
			self.response.append(line.decode('utf-8').replace('\n', ''))

	def get_dictionary(self):
		keys = []
		values = []	

		# locate data position in response
		i = 0
		while i < len(self.response):
			if "$$SOE" in self.response[i]:
				keys = self.response[i - 2].split(",")
				values = self.response[i + 1].split(",")
			i += 1

		# create dictionary
		i = 0
		while i < len(keys):
			self.dictionary[keys[i].strip()] = values[i].strip()
			i += 1

		return self.dictionary

	def get_response(self):
		return self.response
