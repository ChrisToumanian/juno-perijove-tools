#! /usr/bin/python

import sys,os
import curses
from datetime import datetime
import horizons

def draw_menu(stdscr):
	k = 0

	# Declaration of strings
	title = "JUNO DASHBOARD"
	statusbarstr = "Press 'q' to exit. Press any key to update."

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
		stdscr.attroff(curses.color_pair(3))
		stdscr.refresh()

		# Get updates from Horizons
		date = datetime.utcnow()
		request = horizons.HorizonsRequest("672@399", "-61", date, "4,20,21")
		request.send()
		juno_data = request.get_dictionary()
		request = horizons.HorizonsRequest("672@399", "599", date, "4,20,21")
		request.send()
		jupiter_data = request.get_dictionary()

		# Render time
		stdscr.addstr(0, width-len(juno_data["Date__(UT)__HR:MN:SC.fff"] + " (UTC)")-1, juno_data["Date__(UT)__HR:MN:SC.fff"] + " (UTC)")
	
		# Center calculation
		center_x = int(width // 2)
		center_y = int(height // 2)
		
		# Render display Box
		stdscr.addstr(center_y, center_x, "+")
		stdscr.addstr(center_y + 10, center_x - 30, "\u2517")
		stdscr.addstr(center_y - 10, center_x + 30, "\u2513")
		stdscr.addstr(center_y + 10, center_x + 30, "\u251B")
		stdscr.addstr(center_y - 10, center_x - 30, "\u250F")

		# Render Juno
		juno_pos_x = center_x + 8
		juno_pos_y = center_y + 5
		stdscr.addstr(juno_pos_y, juno_pos_x, "\u00A4")

		# Render Jupiter data
		stdscr.addstr(center_y, center_x + 2, "JUPITER", curses.color_pair(1))	
		stdscr.addstr(8, 1, "JUPITER")	
		stdscr.addstr(9, 1, "Apparent Azi/Elev: " + jupiter_data["Azi_(a-app)"] + "," + juno_data["Elev_(a-app)"], curses.color_pair(1))
		stdscr.addstr(10, 1, "Distance (km): " + jupiter_data["delta"], curses.color_pair(1))
		stdscr.addstr(11, 1, "1-way LT (min): " + jupiter_data["1-way_down_LT"], curses.color_pair(1))

		# Render Juno data
		stdscr.addstr(juno_pos_y, juno_pos_x + 2, "JUNO", curses.color_pair(1))
		stdscr.addstr(2, 1, "JUNO")	
		stdscr.addstr(3, 1, "Apparent Azi/Elev: " + juno_data["Azi_(a-app)"] + "," + juno_data["Elev_(a-app)"], curses.color_pair(1))
		stdscr.addstr(4, 1, "Distance (km): " + juno_data["delta"], curses.color_pair(1))
		stdscr.addstr(5, 1, "1-way LT (min): " + juno_data["1-way_down_LT"], curses.color_pair(1))

		# Refresh screen
		stdscr.refresh()

		# Wait for next input
		k = stdscr.getch()

def main():
	curses.wrapper(draw_menu)

main()
