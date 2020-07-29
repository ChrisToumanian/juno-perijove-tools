#! /usr/local/bin/python

import sys
import urllib.request
import math
from datetime import datetime, timedelta

# JPL NAIF spice kernels - predicted orbit
naif_orbit_url = "https://naif.jpl.nasa.gov/pub/naif/JUNO/kernels/spk/juno_pred_orbit.orb"
predicted_orbit = []
selected_line = 1

# JPL HORIZONS ephemerides
horizons_url_1 = "https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&COMMAND='599'&MAKE_EPHEM='YES'&OBJ_DATA='NO'&TABLE_TYPE='OBSERVER'&TLIST='"
horizons_url_2 = "'&CENTER='672@399'&QUANTITIES='2,20,21'&CAL_FORMAT='BOTH'&ANG_FORMAT='DEG'&CSV_FORMAT='YES'"
horizons_data = []

# data
ephemeris_type = "OBSERVER"
target_body = "Jupiter"
observer_location = "Geocentric"
quantities = "2,20,21"
datetime_initial = None
observer_range = ""
one_way_lt = 0
apparent_ra = ""
apparent_dec = ""

# results
pdt_compensation = -7
pst_compensation = -8
datetime_adjusted = None
datetime_pdt = None
datetime_pst = None

def get_julian_datetime(date):
	# Ensure correct format
	if not isinstance(date, datetime):
		raise TypeError('Invalid type for parameter "date" - expecting datetime')
	elif date.year < 1801 or date.year > 2099:
		raise ValueError('Datetime must be between year 1801 and 2099')

	# Perform the calculation
	julian_datetime = 367 * date.year - int((7 * (date.year + int((date.month + 9) / 12.0))) / 4.0) + int((275 * date.month) / 9.0) + date.day + 1721013.5 + (date.hour + date.minute / 60.0 + date.second / math.pow(60,2)) / 24.0 - 0.5 * math.copysign(1, 100 * date.year + date.month - 190002.5) + 0.5

	return julian_datetime

def get_predicted_orbit():
	global predicted_orbit
	file = urllib.request.urlopen(naif_orbit_url)
	for line in file:
		predicted_orbit.append(line.decode('utf-8').replace('\n', ''))

def select_date():
	global selected_line
	global predicted_orbit
	global datetime_initial

	selected_line += int(input("\nSelect perijove no.: "))
	line_str = predicted_orbit[selected_line][51:71]
	datetime_initial = datetime.strptime(predicted_orbit[selected_line][51:71], '%Y %b %d %H:%M:%S')
	print("You selected:", line_str)

def get_horizons_data():
	global horizons_data
	global datetime_initial

	# get Julian date
	juliandate = get_julian_datetime(datetime_initial)

	# create Horizons request
	url = horizons_url_1
	url += str(juliandate)
	url += horizons_url_2

	print("Julian Date:", str(juliandate), "\n")

	# fetch request
	file = urllib.request.urlopen(url)
	for line in file:
		horizons_data.append(line.decode('utf-8').replace('\n', ''))

def get_ephemerides():
	global datetime_initial

	print("")
	#datetime_input = str(input("Enter date & time <YYYY-MM-DD HH:MM:SS>: "))
	#datetime_initial = datetime.strptime(datetime_input, '%Y-%m-%d %H:%M:%S')
	#one_way_lt = float(input("Enter one-way LT (minutes) from ssd.jpl.nasa.gov/horizons.cgi: "))

	# obtain one-way LT from horizons_data
	trimmed_lt = horizons_data[36][106:121].lstrip()
	one_way_lt = float(trimmed_lt)
	print("One-way LT:", str(one_way_lt))
	
	# calculate datetimes adjusted for LT and timezone
	datetime_adjusted = datetime_initial + timedelta(minutes = one_way_lt)
	datetime_pdt = datetime_adjusted + timedelta(hours = pdt_compensation)
	datetime_pst = datetime_adjusted + timedelta(hours = pst_compensation)

	# print results
	print("\nPerijove Obs. Times")
	print("=======================")
	print(datetime_adjusted.strftime('%Y-%m-%d %H:%M:%S'), "UTC")
	print(datetime_pdt.strftime('%Y-%m-%d %H:%M:%S'), "PDT")
	print(datetime_pst.strftime('%Y-%m-%d %H:%M:%S'), "PST")

def main():
	print("JUNO Perijove Dates from naif.jpl.nasa.gov/pub/naif/JUNO/kernels/spk/juno_pred_orbit.orb\n")

	# perijove dates
	get_predicted_orbit()
	for line in predicted_orbit:
		print(line)

	# select date 
	select_date()

	# fetch horizons data
	get_horizons_data()
	i = 0
	while i < 39:
		print(horizons_data[i])
		i += 1

	# ephemerides
	get_ephemerides()
	
main()
