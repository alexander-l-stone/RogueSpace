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
        self.planet_entity = Entity(self.x, self.y, self.char, self.color, {'on_collide'})
        self.system = system
        self.planetary_radius:int = planetary_radius

    def on_collide_system_level(target, initiator):
        return {'type' : 'enter', 'entering_entity' : initiator, 'entering': target}

    def on_collide(target, initiator):
        return {'type': 'stop'}

    def test_for_exit_planetary_area(self, area):
        exit_list = []
        for coord, entity in area.entity_dict.items():
            if math.sqrt(coord[0]**2 + coord[1]**2) > self.planetary_radius:
                exit_list.append({'type': 'exit', 'exiting_entity': entity, 'exiting_too': self.system})
        return exit_list

    def generate_planetary_area(self, entity_list=[]):
        planetary_area = Area()
        for moon in self.moons:
            planetary_area.add_entity(moon)
        for entity in entity_list:
            planetary_area.add_entity(entity)
        for theta in range(0,360):
            x = int(self.planetary_radius*math.cos(theta))
            y = int(self.planetary_radius*math.sin(theta))
            radius_marker = Entity(x, y, '*', (255, 255, 255))
            if (x, y) not in planetary_area.entity_dict:
                planetary_area.add_entity(radius_marker)
        planetary_area.add_entity(Entity(0, 0, self.char, self.color, {'on_collide': self.on_collide}))
        return planetary_area
