from source.entity.entity import Entity
import math

#TODO: Test this class
class Ring:
    def __init__(self, radius:int, char:str, color, flags={}):
        self.radius = radius
        self.char = char
        self.color = color
        self.flags = flags
    
    def generate_entities(self, area):
        for theta in range(0,360):
            x = int((self.radius + 0.5) * math.cos(theta))
            y = int((self.radius  +0.5) * math.sin(theta))
            radius_marker = Entity(x, y, self.char, self.color, flags=self.flags)
            if (x, y) not in area.entity_dict:
                area.add_entity(radius_marker)
    
    def generate_offset_entities(self, area, off_x, off_y):
        for theta in range(0,360):
            x = int((self.radius + 0.5) * math.cos(theta)) + off_x
            y = int((self.radius + 0.5) * math.sin(theta)) + off_y
            radius_marker = Entity(x, y, self.char, self.color, flags=self.flags)
            if (x, y) not in area.entity_dict:
                area.add_entity(radius_marker)