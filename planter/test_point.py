"""Tests the point functionality."""
from point import Point

p = Point(1,1,0)
print(p.dist(Point(2,1,0)))

print(p-Point(1,0,0))

p += Point(0,0,1)
print(p)