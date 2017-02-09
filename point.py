# point.py
#
# Implementations of 2d point and vector classes.
#
# B. Bird - 01/02/2016

import math

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
class Vector2d(Point):
	def __init__(self,x,y):
		Point.__init__(self,x,y)
		
	def __neg__(self):
		return Vector(-self.x,-self.y)
	def __pos__(self):
		return self
		
	def __add__(self,other):
		return Vector2d(self.x+other.x,self.y+other.y)
	def __sub__(self,other):
		return Vector2d(self.x-other.x,self.y-other.y)
	def __rsub__(self,other):
		return Vector2d(other.x-self.x,other.y-self.y)
				
	def __mul__(self,f):
		return Vector2d(self.x*f, self.y*f)
	def __rmul__(self,f):
		return Vector2d(self.x*f, self.y*f)

	def __div__(self,f):
		return Vector2d(self.x/float(f), self.y/float(f))		
		
	def __getitem__(self,key):
		if key == 0:
			return self.x
		if key == 1:
			return self.y
		raise IndexError() 
		
	def __setitem__(self,key,value):
		if key == 0:
			self.x = value
		if key == 1:
			self.y = value
		raise IndexError()
		
	def __str__(self):
		return str(tuple(self))
		
	def dot(self,other):
		return self.x*other.x + self.y*other.y
	
	def length(self):
		return math.sqrt(self.dot(self))
