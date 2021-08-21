import math
from random import seed, randint

from source.draw.area.area import Area
from source.draw.entity.entity import Entity
from source.stellar_objects.belt import Belt
from source.stellar_objects.cloud import Cloud
from source.stellar_objects.ring import Ring
from source.stellar_objects.star import Star


class System:
    def __init__(self, x:int, y:int, char:str, color:tuple, name:str, system_type:str, hyperlimit:int, hot_zone, bio_zone, cold_zone, gas_zone, frozen_zone, bgcolor=(0,0,0), **flags):
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
        self.radius = 1
        self.hot_zone = hot_zone
        self.bio_zone = bio_zone
        self.cold_zone = cold_zone
        self.gas_zone = gas_zone
        self.frozen_zone = frozen_zone
        self.star = Star(0, 0, 1, self.char, self.color, self.name, self.system_type, self.bgcolor, **flags)
        if self.system_type == 'dwarf-red' or self.system_type == 'dwarf-white':
            self.star.radius = 6
        elif self.system_type == 'dwarf-brown':
            self.star.radius = 5
        elif self.system_type == 'giant-red' or self.system_type == 'giant-blue':
            self.star.radius = 10
        else:
            self.star.radius = 7
        self.seed = randint(1, 100) + self.x + self.y
    
    def point_inside(self, x, y):
        self.star.point_inside(x, y)

    def generate_area(self, entity_list=[]):
        system_area = Area(self.bgcolor, name=self.name, generate_background=True)
        for entity in self.entity_list:
            if isinstance(entity, Cloud):
                entity.generate_entities(system_area)
            else:
                system_area.add_entity(entity)
        for planet in self.planet_list:
            if (isinstance(planet, Ring) or isinstance(planet, Belt)):
                planet.generate_entities(system_area)
            else:
                planet.generate_entities(system_area)
        for entity in entity_list:
            if isinstance(entity, Cloud):
                entity.generate_entities(system_area)
            else:
                system_area.add_entity(entity)
        for theta in range(0,360):
            x = int(float(self.hyperlimit)*math.cos(theta))
            y = int(float(self.hyperlimit)*math.sin(theta))
            radius_marker = Entity(x, y, '.', (100, 0,0), self)
            if (x, y) not in system_area.entity_dict:
                system_area.add_entity(radius_marker)
        self.star.generate_entities(system_area)
        return system_area

    def add_planet(self, planet):
        self.planet_list.append(planet)
        planet.system = self

    def on_collide_sector_level(self, target, initiator):
        return {'type' : 'enter', 'entering_entity' : initiator, 'target_entity': self}

    def on_collide(self, target, initiator):
        return {'type': 'stop'}

    def generate_star_entity(self):
        return Entity(self.x, self.y, self.char, self.color, self, on_collide=self.on_collide_sector_level, bg_color=self.bgcolor)
