import json
from math import cos, sin, pi, sqrt
import numpy as np
from shapely.geometry import Polygon

from IFSLibrary import IFSfunc

class Parser:
	base_scaling = 2/(1 + sqrt(5))      #  = 0.618033988749
	@staticmethod
	def parse(filename, **kwargs):
		IFS = []
		A = []
		theta = []

		with open(filename, "r") as f:
			data = json.load(f) 

		if 'IFS' in data.keys():
			IFS, A, theta = Parser.parseIFS(data)
		elif 'rotation' in data.keys():
			IFS.append(Parser.parseIFS(data))

		return [IFS, A, theta]

	@staticmethod
	def parseFunction(data):
		r = data['rotation']
		s = Parser.base_scaling**data['scaling']
		t = data['translation']
		if 'edge' in data:
			edge = data['edge']
		else:
			edge = [0,0]

		c = pi/180 # Degrees -> radians conversion factor

		a = s * cos(c * r);      b = - s * sin(c * r);      e = t[0]
		c = s * sin(c * r);      d = a;                     f = t[1]

		# Matrix = 	[s cos(theta),   -s sin(theta),    x_translation]
		#			[s sin(theta),    s cos(theta),    y_translation]
		#			[     0      ,         0      ,          1      ]
		matrix = np.array([
			[a, b, e],
			[c, d, f],
			[0, 0, 1]
		])

		return IFSfunc(scaling = data['scaling'], matrix = matrix, edge = e)
	
	@staticmethod
	def parseIFS(data):
		if 'base_scaling' in data.keys():
			Parser.base_scaling = data['base_scaling']
		
		IFS = []
		for func in data['IFS']:
			IFS.append(Parser.parseFunction(func))

		A = []
		for attractor in data['A']:
			A.append(Polygon(attractor))

		# theta = data['theta']
		theta = []
		for t in data['theta']:
			if t > len(IFS) or t < 1: # ERROR: theta_i out of bounds
				print(f"ERROR: theta_i is out of bounds.\n\tReceived {t}, but there are only {len(IFS)} functions in the IFS.")
			else:
				theta.append(t)

		return [IFS, A, theta]



