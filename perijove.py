#! /usr/local/bin/python

import sys
import urllib.request
import math
from datetime import datetime, timedelta
import horizons

naif_orbit_url = "https://naif.jpl.nasa.gov/pub/naif/JUNO/kernels/spk/juno_pred_orbit.orb"
predicted_orbit = []
selected_line = 1
ephemerides_dict = {}
one_way_lt = 0
pdt_compensation = -7
pst_compensation = -8
datetime_initial = None
datetime_adjusted = None
datetime_pdt = None
datetime_pst = None

def get_predicted_orbit():
	global predicted_orbit
	file = urllib.request.urlopen(naif_orbit_url)
	for line in file:
		predicted_orbit.append(line.decode('utf-8').replace('\n', ''))

def select_perijove():
	global selected_line
	global predicted_orbit
	global datetime_initial

	selected_line += int(input("\nSelect perijove no.: "))
	line_str = predicted_orbit[selected_line][51:71]
	datetime_initial = datetime.strptime(predicted_orbit[selected_line][51:71], '%Y %b %d %H:%M:%S')
	print("You selected:", line_str)

def get_ephemerides():
	global datetime_initial
	global ephemerides_dict

	# horizons request
	request = horizons.HorizonsRequest("672@399", "599", datetime_initial, "2,20,21")
	request.send()
	ephemerides_dict = request.get_dictionary()

def show_perijove_times():
	global datetime_initial
	global ephemerides_dict

	print("")

	# obtain one-way LT from horizons_dictionary
	one_way_lt = float(ephemerides_dict["1-way_down_LT"])
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

	# select perijove 
	select_perijove()

	# fetch horizons data
	get_ephemerides()

	# ephemerides
	show_perijove_times()
	
main()
