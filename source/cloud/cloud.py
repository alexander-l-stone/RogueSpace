from source.entity.entity import Entity
from random import seed, randint
import math

class Cloud:
    def __init__(self, x, y, char, color, radius, seed):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.radius = radius
        self.seed = seed
    
    def generate_entities(self, area):
        #TODO: Make these contiguous
        randnumber = randint(1, math.pi*self.radius**2//2)
        x = self.x
        y = self.y
        for i in range(randnumber):
            area.add_entity(Entity(x, y, self.char, self.color))
            d2 = randint(1, 2)
            d22 = randint(1, 2)
            #This is the second d2
            if d2 == 1:
                if d22 == 1:
                    dx = 1
                    dy = 0
                else:
                    dx = -1
                    dy = 0
            else:
                if d22 == 1:
                    dx = 0
                    dy = 1
                else:
                    dx = 0
                    dy = -1
            x += dx
            y += dy