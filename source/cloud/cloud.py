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
        seed(self.seed)
        randnumber = randint(1, math.pi*self.radius**2//2)
        angle = 0
        for i in range(randnumber):
            randangle = randint(angle - 45, angle + 45)
            randdistance = randint(0, self.radius)
            area.add_entity(Entity(int((randdistance + 0.5) * math.cos(randangle)) + self.x, int((randdistance + 0.5) * math.cos(randangle)) + self.y, self.char, self.color))
            seed(self.seed + i)
            angle += 90