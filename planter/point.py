class Point(object):
  """Defines point for doing vector arithmetic."""
  def __init__(self,x=0,y=0,z=0):
    self.x = x
    self.y = y
    self.z = z

  def norm(self):
    """Computes norm of point."""
    deltas = [self.x,self.y,self.z]
    return sum([d**2 for d in deltas])**.5


  def dist(self,p2):
    """Computes Euclid distance with p2."""
    deltas = [self.x-p2.x, self.y-p2.y,self.z-p2.z]
    return sum([d**2 for d in deltas])**.5


  def __sub__(self,p2):
    """Return new point of p1-p2."""
    return Point(self.x-p2.x,
                 self.y-p2.y,
                 self.z-p2.z)


  def __add__(self,p2):
    """Return new point of p1+p2."""
    return Point(self.x+p2.x,
                 self.y+p2.y,
                 self.z+p2.z)

  def __iadd__(self,p2):
    self.x += p2.x
    self.y += p2.y
    self.z += p2.z
    return self

  def __isub__(self,p2):
    self.x -= p2.x
    self.y -= p2.y
    self.z -= p2.z
    return self


  def __repr__(self):
    return f"<X:{self.x}, Y:{self.y}, Z:{self.z}>"

