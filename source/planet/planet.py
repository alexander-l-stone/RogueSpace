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
        self.system = system
        self.planetary_radius:int = planetary_radius
        self.entity_list = []
        self.bgcolor = bgcolor

    def generate_planetary_entity(self):
        return Entity(self.x, self.y, self.char, self.color, flags={'bg_color': self.bgcolor})

    def on_collide(self, target, initiator):
        return {'type': 'stop'}
    
    def generate_entities(self, area):
        area.add_entity(Entity(self.x, self.y, self.char, self.color))
        for moon in self.moons:
            area.add_entity(moon.generate_offset_entity(self.x, self.y))
        for planetary_entity in self.entity_list:
            if (isinstance(planetary_entity, Ring)):
                planetary_entity.generate_offset_entities(area, self.x, self.y)
            else:
                area.add_entity(planetary_entity)
