from source.draw.entity.entity import Entity
from random import randint, seed

class Star:
    def __init__(self, x:int, y:int, radius:int, char:str, color:tuple, name:str, star_type:str, bgcolor:tuple, **flags):
        self.x = x
        self.y = y
        self.radius = radius
        self.char = char
        self.color = color
        self.name = name
        self.star_type = star_type
        self.flags = flags
        self.bgcolor = bgcolor
        self.entity_list = []
        
    def __str__(self):
        return f"[Star]"
    
    def __repr__(self) -> str:
        return f"[Star]"

    def point_inside(self, x, y):
        dx = abs(x - self.x)
        dy = abs(y - self.y)
        tempradius = self.radius + 0.5
        if self.radius <= 2:
            return dx**2 + dy**2 <= tempradius**2
        else:
            return dx**2 + dy**2 < tempradius**2
    
    def generate_entities(self, system_area):
        for x in range(-1 * self.radius, self.radius + 1):
            for y in range(-1 * self.radius, self.radius + 1):
                if self.point_inside(x, y):
                    new = Entity(x,y,self.char,self.color,self)
                    self.entity_list.append(new)
                    system_area.add_entity(new)

    def generate_entity(self, x, y):
        seed(randint(1, 100) + x + y)
        num_frames = randint(1, 4)
        color_frames = [self.color]
        for i in range(num_frames):
            red = randint(max(0,self.color[0]-25), min(255, self.color[0]+25))
            green = randint(max(0,self.color[1]-25), min(255, self.color[1]+25))
            blue = randint(max(0,self.color[2]-25), min(255, self.color[2]+25))
            color_frames.append((red, green, blue))
        return Entity(x, y, self.char, color_frames, self, bg_color=self.bgcolor)