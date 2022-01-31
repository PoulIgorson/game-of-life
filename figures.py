class Point:
  def __init__(self):
    self.fig = []
    
  def set_in_field(self, field, x=0, y=0):
    for i in range(len(self.fig)):
      for j in range(len(self.fig[0])):
        field[y + i][x + j] = self.fig[i][j]


class Flasher(Point):
  def __init__(self):
    self.fig = [
      [0, 0, 0],
      [1, 1, 1],
      [0, 0, 0]
    ]


from random import random
def randomfield(field, proc):
  for i in range(len(field)):
    for j in range(len(field[0])):
      field[i][j] = int(random()*100 < proc)
  return field