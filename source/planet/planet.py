from source.entity.entity import Entity
from source.area.area import Area
from source.planet.moon import Moon
from source.ring.ring import Ring
import math

class Planet:
    def __init__(self, x:int, y:int, char:str, color:tuple, name:str, planet_type:str, system, planetary_radius:int, moons = None, bgcolor=(0,0,0)):
        self.char:str = char
        self.x = x
        self.y = y
        self.color:tuple = color
        self.planet_type:str = planet_type
        if moons is None:
            self.moons = []
        else:
            self.moons = moons
        self.name = name
        self.planet_entity = Entity(self.x, self.y, self.char, self.color, {'on_collide': self.on_collide_system_level})
        self.system = system
        self.planetary_radius:int = planetary_radius
        self.entity_list = []
        self.bgcolor = bgcolor

    def generate_planetary_entity(self):
        return Entity(self.x, self.y, self.char, self.color, flags={'on_collide': self.on_collide_system_level, 'bg_color': self.bgcolor})

    def on_collide_system_level(self, target, initiator):
        return {'type' : 'enter', 'entering_entity' : initiator, 'target_entity': self}

    def on_collide(self, target, initiator):
        return {'type': 'stop'}

    def test_for_exit_planetary_area(self, area):
        exit_list = []
        for coord, entities in area.entity_dict.items():
            if math.sqrt(coord[0]**2 + coord[1]**2) > self.planetary_radius:
                for entity in entities:
                    exit_list.append({'type': 'exit', 'exiting_entity': entity, 'exiting_too': self.system})
        return exit_list

    def generate_area(self, entity_list=[]):
        planetary_area = Area(self.bgcolor)
        for moon in self.moons:
            planetary_area.add_entity(moon.generate_entity())
        for planetary_entity in self.entity_list:
            if (isinstance(planetary_entity, Ring)):
                planetary_entity.generate_entities(planetary_area)
            else:
                planetary_area.add_entity(planetary_entity)
        for entity in entity_list:
            planetary_area.add_entity(entity)
        for theta in range(0,360):
            x = int(self.planetary_radius*math.cos(theta))
            y = int(self.planetary_radius*math.sin(theta))
            radius_marker = Entity(x, y, 'x', (0, 255, 0))
            if (x, y) not in planetary_area.entity_dict:
                planetary_area.add_entity(radius_marker)
        planetary_area.add_entity(Entity(0, 0, self.char, self.color, {'on_collide': self.on_collide}))
        return planetary_area
