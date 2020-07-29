#! /usr/local/bin/python

import horizons
from datetime import datetime

date = datetime.utcnow()

request = horizons.HorizonsRequest("672@399", "599", date, "2,20,21")

request.send()

response = request.get_response()

# for line in response:
#	print(line)

dictionary = request.get_dictionary()

for key in dictionary:
	print(key, ":", dictionary[key])
