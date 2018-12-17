import math
import numpy  as np

from EMD import EMD

class Point:
   def __init__( self, x=0, y=0):
      self.x = x
      self.y = y

#finds the distance between the two given points
def dist(p0,p1):
	return math.sqrt((p1.x - p0.x)**2 + (p1.y - p0.y)**2)

class Sequence:
	#This class stores Mouse Move Sequence for a valid session.
	def __init__(self, p=[], t=[]):
		self.p = p
		self.t = t
		self.size = 0
		self.sig = []
	def __del__(self):
		del self.p
		del self.t
		del self.size
		del self.sig

	def add_p(self,P,t):
		self.p.append(P)
		self.t.append(t)
		self.size = self.size + 1

	def get_sig(self):
		if len(self.p) is not 0:
			x1 = self.p[0].x
			y1 = self.p[0].y
			x2 = self.p[-1].x
			y2 = self.p[-1].y
			if(dist(self.p[0],self.p[-1]) == 0):
				return [],[]
			else:
				for p in self.p:
					self.sig.append(((y2-y1)*p.x+(x1-x2)*p.y+y1*x2-y2*x1)/dist(self.p[0],self.p[-1]))
			return self.sig,self.t	
	def get_p(self):
		return self.p,self.t
	def get_size(self):
		return self.size	

	def get_emd(self):
		self.imf = EMD().emd(self.sig,self.t)
	def get_start(self):
		return self.p[0]
	def get_end(self):
		return self.p[-1]



