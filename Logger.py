"""Class that creates logs for variables.

TODO:
1. Add a new object, called "Variable."  Let this
object have properties such as name, value, last update, etc.
"""
import datetime
import json

class Logger(object):
	def __init__(self,filename='log'):
		self.temp = None
		self.EC = None
		self.filename = filename

	def clearVariables(self):
		"""Resets all variables to None."""
		self.temp = None
		self.EC = None

	
	def parseInput(self,line):
		"""Parses the input according to custom protocol.  
		Stores the appropriate values in the logger object."""

		# Custom protocol
		TEMP_PRE = 'Temp'
		EC_PRE = 'EC'

		if line[0] == "": # nothing to parse 
			return 
		elif line.startswith( TEMP_PRE ):
			self.temp = line[len(TEMP_PRE):]
		elif line.startswith( EC_PRE):
			self.EC = line[len(EC_PRE):]


	def createLogDict(self):
		"""Creates of dictionary of variables.  Only stores variables
		that are non-empty.  Also adds the timestamp."""

		result = dict()

		# logs variables
		if self.temp is not None:
			result['Temp'] = self.temp
		if self.EC is not None:
			result['EC'] = self.EC

		# include timestamp
		result['Timestamp'] = str(datetime.datetime.now())

		return result


	def log(self):
		"""Logs the current variables in the log file.  
		Checks that the log will be non-empty."""

		toLog = self.createLogDict()
		if len(toLog) > 1: #checks for something to log
			f = open(self.filename,'a')
			f.write(json.dumps(toLog)+'\n')
			f.close()

			self.clearVariables() # remove stale states
