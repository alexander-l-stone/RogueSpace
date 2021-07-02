from source.area.area import Area
from source.entity.entity import Entity
import math

class System:
    def __init__(self, x:int, y:int, char:str, color:tuple, name:str, system_type:str, hyperlimit:int, sector=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.system_type = system_type
        self.hyperlimit = hyperlimit
        self.sector = sector
        self.planet_list = []
        self.entity_list = []
    
    def generate_system_area(self, entity_list=[]):
        system_area = Area()
        for system_entity in self.entity_list:
            system_area.add_entity(system_entity)
        for entity in entity_list:
            system_area.add_entity(entity)
        for theta in range(0,360):
            x = int(self.hyperlimit*math.cos(theta))
            y = int(self.hyperlimit*math.sin(theta))
            radius_marker = Entity(x, y, '*', (100, 0,0))
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
        return Entity(self.x, self.y, self.char, self.color, flags={'on_collide': self.on_collide_sector_level})
