#! /usr/bin/python

import sys,os
import curses
from datetime import datetime, timedelta
import system

def draw_menu(stdscr):
	k = 0
	zoom = 55
	lt_minutes = 0
	selected_object = 4

	# Declaration of strings
	title = "JUNO DASHBOARD"
	statusbarstr = " Press 'q' to exit | Press 'u' to update | Press 'n' for next object | +/- to zoom"

	# Clear and refresh screen
	stdscr.clear()
	curses.curs_set(0)

	# Start colors in curses
	curses.start_color()
	curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

	# Set up system
	sol_system = system.System()
	sol_system.set_observer_code("672@399")
	sol_system.add_object("Io", "501", "4,20,21", "\u00B0")
	sol_system.add_object("Europa", "502", "4,20,21", "\u00B0")
	sol_system.add_object("Ganymede", "503", "4,20,21", "\u00B0")
	sol_system.add_object("Jupiter", "599", "4,20,21", "\u00A4")
	sol_system.add_object("Juno", "-61", "4,20,21", "Y")

	# Object notes
	sol_system.get_object("Juno").notes = "Launch: Aug 5, 2011 16:25 UTC\nEarth Flyby: Oct 9, 2013 19:21:25 UTC\nArrive Jupiter: Jul 5, 2016 02:30 UTC\nDimensions: 20m\nSolar-powered, spin-stabilized spacecraft\nThree 2x9m solar panels around hexagonal bus\nGravity/radio science system\nSix-wavelength microwave radiometer\nVector magnetometer\nPlasma and energetic particle detectors\nRadio/plasma wave experiment\nUltraviolet imager/spectrometer\nInfrared imager/spectrometer\nBipropellant engine\nRCS thrusters"

	# First update
	sol_system.set_datetime_utc(datetime.utcnow())
	sol_system.update()
	jupiter = sol_system.get_object("Jupiter")

	# Loop where k is the last character pressed
	while (k != ord('q')):

		# Select next object
		if (k == ord('n')):
			selected_object += 1
			if (selected_object == len(sol_system.objects)):
				selected_object = 0

		# Check zoom
		if (k == ord('+')):
			zoom *= 1.5
			zoom = int(zoom)
		elif (k == ord('-')):
			zoom *= 0.75
			zoom = int(zoom)
		if (zoom < 2):
			zoom = 2

		# Initialization
		stdscr.clear()
		height, width = stdscr.getmaxyx()

		# Render title
		stdscr.attron(curses.color_pair(2))
		stdscr.attron(curses.A_BOLD)
		stdscr.addstr(0, 0, title)
		stdscr.attroff(curses.color_pair(2))
		stdscr.attroff(curses.A_BOLD)

		# Render status bar
		stdscr.attron(curses.color_pair(3))
		stdscr.addstr(height-1, 0, statusbarstr)
		stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
		stdscr.addstr(height-1, width-15, "ZOOM: ")
		stdscr.addstr(height-1, width-10, str(zoom))
		stdscr.attroff(curses.color_pair(3))

		# Update system
		if (k == ord('u')):
			sol_system.set_datetime_utc(datetime.utcnow() - timedelta(minutes = lt_minutes))
			sol_system.update()

		# Render time
		date = jupiter.get_value("Date__(UT)__HR:MN:SC.fff")
		lt = jupiter.get_value("1-way_down_LT")
		stdscr.addstr(0, width-len(date + " (UTC)")-1, date + " (UTC)")
		if (lt_minutes == 0):
			lt_minutes = float(lt)
	
		# Center calculation
		center_x = int(width // 2)
		center_y = int(height // 2)
		
		# Render display Box
		stdscr.addstr(height - 5, 8, "\u2517") # lower-left
		stdscr.addstr(5, width - 8, "\u2513") # upper-right
		stdscr.addstr(height - 5, width - 8, "\u251B") # lower-right
		stdscr.addstr(5, 8, "\u250F") # upper-left

		# Render objects
		for obj in sol_system.objects:
			offset_deg_x = float(obj.get_value("Azi_(a-app)")) - float(jupiter.get_value("Azi_(a-app)"))
			offset_deg_y = float(obj.get_value("Elev_(a-app)")) - float(jupiter.get_value("Elev_(a-app)"))
			pos_x = center_x + int(offset_deg_x * zoom)
			pos_y = center_y - int(offset_deg_y * (zoom / 2))
			if (pos_x > 0 and pos_x < width - len(obj.name) - 1 and pos_y > 0 and pos_y < height - 1):
				stdscr.addstr(pos_y, pos_x, obj.symbol)
				if (sol_system.objects[selected_object].name == obj.name):
					stdscr.addstr(pos_y, pos_x + 2, obj.name.upper(), curses.color_pair(4))
				else:
					stdscr.addstr(pos_y, pos_x + 2, obj.name.upper(), curses.color_pair(1))

		# Render selected object data
		obj = sol_system.objects[selected_object]
		z_distance = float(obj.get_value("delta")) - float(jupiter.get_value("delta"))
		
		stdscr.addstr(2, 0, obj.name)	
		stdscr.addstr(3, 0, "Apparent Azi/Elev: " + obj.get_value("Azi_(a-app)") + ", " + obj.get_value("Elev_(a-app)"), curses.color_pair(1))
		stdscr.addstr(4, 0, "Distance: " + obj.get_value("delta") + " km", curses.color_pair(1))
		stdscr.addstr(5, 0, "1-way LT: " + obj.get_value("1-way_down_LT") + " min", curses.color_pair(1))
		stdscr.addstr(6, 0, "Z-distance from Jupiter: " + str(z_distance) + " km", curses.color_pair(1))
		stdscr.addstr(8, 0, obj.notes, curses.color_pair(1))
		
		# Refresh screen
		stdscr.refresh()

		# Wait for next input
		k = stdscr.getch()

def main():
	curses.wrapper(draw_menu)

main()
