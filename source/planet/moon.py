from source.entity.entity import Entity

class Moon:
    def __init__(self, x:int, y:int, char:str, color:tuple, moon_type:str, name:str, planet, flags={}):
        self.x = x
        self.y = y
        self.planet = planet
        self.char = char
        self.color = color
        self.flags = flags
        self.moon_type = moon_type
        self.name = name
    
    def generate_entity(self):
        return Entity(self.x, self.y, self.char, self.color, self.flags)
