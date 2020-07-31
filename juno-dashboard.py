#! /usr/bin/python

import sys,os
import curses
from datetime import datetime, timedelta
import horizons

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

	# Declaration of strings
	title = "JUNO DASHBOARD"
	statusbarstr = "Press 'q' to exit  |  Press any key to update  |  Press +/- to zoom"

	# Clear and refresh screen
	stdscr.clear()
	stdscr.refresh()
	curses.curs_set(0)

	# Start colors in curses
	curses.start_color()
	curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

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
		stdscr.refresh()

		# Get updates from Horizons
		date = datetime.utcnow()
		date = date - timedelta(minutes = lt_minutes)

		request = horizons.HorizonsRequest("672@399", "-61", date, "4,20,21")
		request.send()
		juno_data = request.get_dictionary()
		
		request = horizons.HorizonsRequest("672@399", "599", date, "4,20,21")
		request.send()
		jupiter_data = request.get_dictionary()
	
		request = horizons.HorizonsRequest("672@399", "501", date, "4")
		request.send()
		io_data = request.get_dictionary()
	
		request = horizons.HorizonsRequest("672@399", "502", date, "4")
		request.send()
		europa_data = request.get_dictionary()

		request = horizons.HorizonsRequest("672@399", "503", date, "4")
		request.send()
		ganymede_data = request.get_dictionary()

		# Render time
		stdscr.addstr(0, width-len(juno_data["Date__(UT)__HR:MN:SC.fff"] + " (UTC)")-1, juno_data["Date__(UT)__HR:MN:SC.fff"] + " (UTC)")
		if (lt_minutes == 0):
			lt_minutes = float(juno_data["1-way_down_LT"])
	
		# Center calculation
		center_x = int(width // 2)
		center_y = int(height // 2)
		
		# Render display Box
		stdscr.addstr(center_y + 15, center_x - 40, "\u2517")
		stdscr.addstr(center_y - 15, center_x + 40, "\u2513")
		stdscr.addstr(center_y + 15, center_x + 40, "\u251B")
		stdscr.addstr(center_y - 15, center_x - 40, "\u250F")

		# Render Ganymede
		ganymede_offset_deg_x = float(ganymede_data["Azi_(a-app)"]) - float(jupiter_data["Azi_(a-app)"])
		ganymede_offset_deg_y = float(ganymede_data["Elev_(a-app)"]) - float(jupiter_data["Elev_(a-app)"])
		ganymede_pos_x = limit_pos(center_x + int(ganymede_offset_deg_x * zoom), width)
		ganymede_pos_y = limit_pos(center_y - int(ganymede_offset_deg_y * (zoom / 2)), height)
		stdscr.addstr(ganymede_pos_y, ganymede_pos_x, "\u00B0")
		stdscr.addstr(ganymede_pos_y, ganymede_pos_x + 1, "GANYMEDE", curses.color_pair(1))	

		# Render Europa
		europa_offset_deg_x = float(europa_data["Azi_(a-app)"]) - float(jupiter_data["Azi_(a-app)"])
		europa_offset_deg_y = float(europa_data["Elev_(a-app)"]) - float(jupiter_data["Elev_(a-app)"])
		europa_pos_x = limit_pos(center_x + int(europa_offset_deg_x * zoom), width)
		europa_pos_y = limit_pos(center_y - int(europa_offset_deg_y * (zoom / 2)), height)
		stdscr.addstr(europa_pos_y, europa_pos_x, "\u00B0")
		stdscr.addstr(europa_pos_y, europa_pos_x + 1, "EUROPA", curses.color_pair(1))	

		# Render Io 
		io_offset_deg_x = float(io_data["Azi_(a-app)"]) - float(jupiter_data["Azi_(a-app)"])
		io_offset_deg_y = float(io_data["Elev_(a-app)"]) - float(jupiter_data["Elev_(a-app)"])
		io_pos_x = limit_pos(center_x + int(io_offset_deg_x * zoom), width)
		io_pos_y = limit_pos(center_y - int(io_offset_deg_y * (zoom / 2)), height)
		stdscr.addstr(io_pos_y, io_pos_x, "\u00B0")
		stdscr.addstr(io_pos_y, io_pos_x + 1, "IO", curses.color_pair(1))	

		# Render Jupiter
		stdscr.addstr(center_y, center_x, "\u00A4")

		# Render Juno
		juno_offset_deg_x = float(juno_data["Azi_(a-app)"]) - float(jupiter_data["Azi_(a-app)"])
		juno_offset_deg_y = float(juno_data["Elev_(a-app)"]) - float(jupiter_data["Elev_(a-app)"])
		juno_pos_x = limit_pos(center_x + int(juno_offset_deg_x * zoom), width)
		juno_pos_y = limit_pos(center_y - int(juno_offset_deg_y * (zoom / 2)), height)
		stdscr.addstr(juno_pos_y, juno_pos_x, "Y")

		# Render Jupiter data
		stdscr.addstr(center_y, center_x + 1, "JUPITER", curses.color_pair(1))	
		stdscr.addstr(8, 1, "JUPITER")	
		stdscr.addstr(9, 1, "Apparent Azi/Elev: " + jupiter_data["Azi_(a-app)"] + "," + jupiter_data["Elev_(a-app)"], curses.color_pair(1))
		stdscr.addstr(10, 1, "Distance (km): " + jupiter_data["delta"], curses.color_pair(1))
		stdscr.addstr(11, 1, "1-way LT (min): " + jupiter_data["1-way_down_LT"], curses.color_pair(1))

		# Render Juno data
		stdscr.addstr(juno_pos_y, juno_pos_x + 1, "JUNO", curses.color_pair(1))
		stdscr.addstr(2, 1, "JUNO")	
		stdscr.addstr(3, 1, "Apparent Azi/Elev: " + juno_data["Azi_(a-app)"] + "," + juno_data["Elev_(a-app)"], curses.color_pair(1))
		stdscr.addstr(4, 1, "Distance (km): " + juno_data["delta"], curses.color_pair(1))
		stdscr.addstr(5, 1, "1-way LT (min): " + juno_data["1-way_down_LT"], curses.color_pair(1))

		# Render moon data
		stdscr.addstr(14, 1, "MOONS")
		stdscr.addstr(15, 1, "IO: " + io_data["Azi_(a-app)"] + "," + io_data["Elev_(a-app)"], curses.color_pair(1))
		stdscr.addstr(16, 1, "EUROPA: " + europa_data["Azi_(a-app)"] + "," + europa_data["Elev_(a-app)"], curses.color_pair(1))
		stdscr.addstr(17, 1, "GANYMEDE: " + ganymede_data["Azi_(a-app)"] + "," + ganymede_data["Elev_(a-app)"], curses.color_pair(1))
		
		# Refresh screen
		stdscr.refresh()

		# Wait for next input
		k = stdscr.getch()

def main():
	curses.wrapper(draw_menu)

main()
