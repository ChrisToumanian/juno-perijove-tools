#! /usr/bin/python

import sys
import math
from datetime import datetime, timedelta
import horizons

class Object:
	def __init__(self, name, code, quantities, symbol):
		self.name = name
		self.code = code
		self.quantities = quantities
		self.symbol = symbol
		self.data = {}

	def get_value(self, key):
		for entry in self.data:
			if (entry == key):
				return self.data[key]
		return None

class System:
	def __init__(self):
		self.objects = []
		self.observer_code = None
		self.datetime_utc = datetime.utcnow()

	def add_object(self, name, code, quantities, symbol):
		obj = Object(name, code, quantities, symbol)
		self.objects.append(obj)

	def set_datetime_utc(self, dtime):
		self.datetime_utc = dtime

	def set_observer_code(self, code):
		self.observer_code = code

	def update(self):
		for obj in self.objects:
			request = horizons.HorizonsRequest(self.observer_code, obj.code, self.datetime_utc, obj.quantities)
			request.send()
			obj.data = request.get_dictionary()

	def print_objects(self):
		for obj in self.objects:
			print(obj.name)

	def get_object(self, name):
		for obj in self.objects:
			if (obj.name == name):
				return obj
		return None
