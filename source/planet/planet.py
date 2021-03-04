from source.entity.entity import Entity
from source.area.area import Area
import math

class Planet:
    def __init__(self, x:int, y:int, char:str, color:tuple, name:str, planet_type:str, system, planetary_radius:int, moons = []):
        self.char:str = char
        self.x = x
        self.y = y
        self.color:tuple = color
        self.planet_type:str = planet_type
        self.moons = moons
        self.name = name
        #self.planet_entity
        self.system = system
        self.planetary_radius:int = planetary_radius

    def generate_planetary_area(self, entity_list=[]):
        planetary_area = Area()
        for moon in self.moons:
            planetary_area.add_entity(moon)
        for entity in entity_list:
            planetary_area.add_entity(entity)
        for theta in range(0,360):
            x = int(self.radius*math.cos(theta))
            y = int(self.radius*math.sin(theta))
            radius_marker = Entity(x, y, '*', (255, 255, 255))
            if (x, y) not in planetary_area.entity_dict:
                planetary_area.add_entity(radius_marker)
        return planetary_area
