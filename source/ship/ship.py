from source.ship.ship_components.newtonian_mover import NewtonianMover
from source.draw.entity.entity import Entity
from source.ui.ui_bar import UIBar
from source.ui.ui_message import UIMessage

class Ship:
    def __init__(self, char:str, color:tuple, **flags):
        self.char = char
        self.color = color
        self.flags = flags
        self.x = 0.0
        self.y = 0.0
        self.entity_repr = Entity(0, 0, self.char, self.color, self, **self.flags)
        self.max_fuel = 100
        self.max_health = 50
        self.max_heat = 50
        self.fuel = self.max_fuel
        self.health = 4
        self.heat = 36
        self.path = []
        self.engine = NewtonianMover(self, {'x':0, 'y':0})
    
    def __str__(self):
        return f"[Ship]"
    
    def __repr__(self) -> str:
        return f"[Ship]"

    def thrust(self, dx, dy):
        fuel_cost = abs(dx) + abs(dy)
        if fuel_cost > self.fuel:
            self.engine.thrust(0, 0)
        else:
            self.fuel -= fuel_cost
            self.engine.thrust(dx, dy)

    def get_x(self):
        return round(self.x)
    
    def get_y(self):
        return round(self.y)

    def relocate(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.entity_repr.update_area_position()
        for entity in self.path:
            entity.update_area_position()