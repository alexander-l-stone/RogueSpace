from source.entity.entity import Entity
from random import seed, randint
import math

class Belt:
    def __init__(self, radius:int, char:str, width:int, color:tuple, seed:int, **flags):
        self.radius = radius
        self.char = char
        self.width = width
        self.color = color
        self.flags = flags
        self.seed = seed
    
    def generate_entities(self, area):
        seed(self.seed)
        for theta in range(0,360):
            d10 = randint(1, 10)
            if d10 < 9:
                num_rocks = randint(1, 4)
                for i in range(num_rocks):
                    randwidth = randint(self.radius - self.width//2, self.radius + self.width//2)
                    x = int((self.radius + 0.5 + randwidth) * math.cos(theta))
                    y = int((self.radius + 0.5 + randwidth) * math.sin(theta))
                    radius_marker = Entity(x, y, self.char, self.color, flags=self.flags)
                    overlap = False
                    if (x, y) in area.entity_dict:
                        overlap = True
                    for mte in area.multitileentitylist:
                        if mte.point_inside(x, y):
                            overlap = True
                            break
                    if not overlap:
                        area.add_entity(radius_marker)

    
    #TODO: Turn this into a Belt not a ring method
    # def generate_offset_entities(self, area, off_x, off_y):
    #     for theta in range(0,360):
    #         x = int((self.radius + 0.5) * math.cos(theta)) + off_x
    #         y = int((self.radius + 0.5) * math.sin(theta)) + off_y
    #         radius_marker = Entity(x, y, self.char, self.color, flags=self.flags)
    #         if (x, y) not in area.entity_dict:
    #             area.add_entity(radius_marker)