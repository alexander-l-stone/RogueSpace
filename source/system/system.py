from source.area.area import Area
from source.entity.entity import Entity
from source.ring.ring import Ring
import math

class System:
    def __init__(self, x:int, y:int, char:str, color:tuple, name:str, system_type:str, hyperlimit:int, bgcolor=(0,0,0)):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.system_type = system_type
        self.hyperlimit = hyperlimit
        self.planet_list = []
        self.entity_list = []
        self.bgcolor = bgcolor
        self.explored = False
    
    def generate_area(self, entity_list=[]):
        system_area = Area(self.bgcolor)
        for planet in self.planet_list:
            if (isinstance(planet, Ring)):
                planet.generate_entities(system_area)
            else:
                system_area.add_entity(planet.generate_planetary_entity())
        for entity in entity_list:
            system_area.add_entity(entity)
        for theta in range(0,360):
            x = int(float(self.hyperlimit)*math.cos(theta))
            y = int(float(self.hyperlimit)*math.sin(theta))
            radius_marker = Entity(x, y, 'x', (100, 0,0))
            if (x, y) not in system_area.entity_dict:
                system_area.add_entity(radius_marker)
        system_area.add_entity(Entity(0, 0, self.char, self.color, {'on_collide': self.on_collide}))
        return system_area

    def add_planet(self, planet):
        self.planet_list.append(planet)
        planet.system = self

    def on_collide_sector_level(self, target, initiator):
        return {'type' : 'enter', 'entering_entity' : initiator, 'target_entity': self}

    def on_collide(self, target, initiator):
        return {'type': 'stop'}

    def generate_star_entity(self):
        return Entity(self.x, self.y, self.char, self.color, flags={'on_collide': self.on_collide_sector_level, 'bg_color': self.bgcolor})