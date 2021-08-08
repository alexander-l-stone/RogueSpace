from source.entity.newtonian_entity import NewtonianEntity
from source.ui.ui_bar import UIBar
from source.ui.ui_message import UIMessage

class Ship:
    def __init__(self, char:str, color:tuple, **flags):
        self.char = char
        self.color = color
        self.flags = flags
        self.entity_repr = NewtonianEntity(0, 0, self.char, self.color, self, None, {'x': 0, 'y': 0}, **self.flags)
        self.max_fuel = 100
        self.max_health = 50
        self.max_heat = 50
        self.fuel = self.max_fuel
        self.health = 4
        self.heat = 36
        self.thrust = {'x': 1, 'y': 1} #currently unused

    def thrust(self, dx, dy):
        fuel_cost = dx + dy
        if fuel_cost > self.fuel:
            self.entity_repr.thrust(0, 0)
        else:
            self.fuel -= fuel_cost
            self.entity_repr.thrust(dx, dy)
