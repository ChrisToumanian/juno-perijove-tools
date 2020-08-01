#! /usr/bin/python

import sys,os
import curses
from datetime import datetime, timedelta
import system

def limit_pos(pos, maximum):
	if (pos > maximum):
		pos = maximum - 10
	elif (pos < 1):
		pos = 4
	return pos

def draw_menu(stdscr):
	k = 0
	zoom = 55
	lt_minutes = 0
	selected_object = "Jupiter"

	# Declaration of strings
	title = "JUNO DASHBOARD"
	statusbarstr = " Press 'q' to exit | Press 'u' to update | +/- to zoom"

	# Clear and refresh screen
	stdscr.clear()
	curses.curs_set(0)

	# Start colors in curses
	curses.start_color()
	curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

	# Set up system
	sol_system = system.System()
	sol_system.set_observer_code("672@399")
	sol_system.add_object("Jupiter", "599", "4,20,21", "\u00A4")
	sol_system.add_object("Juno", "-61", "4,20,21", "Y")
	sol_system.add_object("Io", "501", "4,20,21", "\u00B0")
	sol_system.add_object("Europa", "502", "4,20,21", "\u00B0")
	sol_system.add_object("Ganymede", "503", "4,20,21", "\u00B0")

	# First update
	sol_system.set_datetime_utc(datetime.utcnow() - timedelta(minutes = lt_minutes))
	sol_system.update()
	jupiter = sol_system.get_object("Jupiter")

	# Loop where k is the last character pressed
	while (k != ord('q')):
	
		# Check zoom
		if (k == ord('+')):
			zoom *= 1.5
			zoom = int(zoom)
		elif (k == ord('-')):
			zoom *= 0.75
			zoom = int(zoom)

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
		stdscr.addstr(0, width-len(date + " (UTC)")-1, lt + " (UTC)")
		if (lt_minutes == 0):
			lt_minutes = float(lt)
	
		# Center calculation
		center_x = int(width // 2)
		center_y = int(height // 2)
		
		# Render display Box
		stdscr.addstr(center_y + 15, center_x - 40, "\u2517")
		stdscr.addstr(center_y - 15, center_x + 40, "\u2513")
		stdscr.addstr(center_y + 15, center_x + 40, "\u251B")
		stdscr.addstr(center_y - 15, center_x - 40, "\u250F")

		# Render objects
		for obj in sol_system.objects:
			offset_deg_x = float(obj.get_value("Azi_(a-app)")) - float(jupiter.get_value("Azi_(a-app)"))
			offset_deg_y = float(obj.get_value("Elev_(a-app)")) - float(jupiter.get_value("Elev_(a-app)"))
			pos_x = limit_pos(center_x + int(offset_deg_x * zoom), width)
			pos_y = limit_pos(center_y - int(offset_deg_y * (zoom / 2)), height)
			stdscr.addstr(pos_y, pos_x, obj.symbol)
			stdscr.addstr(pos_y, pos_x + 2, obj.name, curses.color_pair(1))

		# Render Jupiter
		stdscr.addstr(center_y, center_x, jupiter.symbol)
		stdscr.addstr(center_y, center_x + 2, jupiter.name, curses.color_pair(1))	

		# Render selected object data
		obj = sol_system.get_object(selected_object)
		stdscr.addstr(8, 1, obj.name)	
		stdscr.addstr(9, 1, "Apparent Azi/Elev: " + obj.get_value("Azi_(a-app)") + "," + obj.get_value("Elev_(a-app)"), curses.color_pair(1))
		stdscr.addstr(10, 1, "Distance (km): " + obj.get_value("delta"), curses.color_pair(1))
		stdscr.addstr(11, 1, "1-way LT (min): " + obj.get_value("1-way_down_LT"), curses.color_pair(1))

		# Refresh screen
		stdscr.refresh()

		# Wait for next input
		k = stdscr.getch()

def main():
	curses.wrapper(draw_menu)

main()
