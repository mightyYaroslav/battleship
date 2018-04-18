import math


class Point:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

	def __str__(self):
		return "x: " + str(self.x) + " y: " + str(self.y)

	def __lt__(self, other):
		if isinstance(other, Point):
			return self.x < other.x and self.y < other.y
		return NotImplemented

	def __le__(self, other):
		if isinstance(other, Point):
			return self.x <= other.x and self.y <= other.y
		return NotImplemented

	def __gt__(self, other):
		if isinstance(other, Point):
			return self.x > other.x and self.y > other.y
		return NotImplemented

	def __ge__(self, other):
		if isinstance(other, Point):
			return self.x >= other.x and self.y >= other.y
		return NotImplemented

	def __eq__(self, other):
		if isinstance(other, Point):
			return self.x == other.x and self.y == other.y
		return NotImplemented

	def __nq__(self, other):
		if isinstance(other, Point):
			return self.x != other.x and self.y != other.y
		return NotImplemented

	def distance(self, p):
		return math.sqrt((self.x - p.x)**2 + (self.y - p.y)**2)

