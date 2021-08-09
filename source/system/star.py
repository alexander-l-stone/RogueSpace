from source.entity.entity import Entity
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
    
    def point_inside(self, x, y):
        dx = abs(x - self.x)
        dy = abs(y - self.y)
        tempradius = self.radius + 0.5
        if self.radius <= 2:
            return dx**2 + dy**2 <= tempradius**2
        else:
            return dx**2 + dy**2 < tempradius**2
    
    def generate_entities(self, system_area):
        for x in range(self.x - self.radius, self.x + self.radius + 1):
            for y in range(self.y - self.radius, self.y + self.radius + 1):
                if self.point_inside(x, y):
                    system_area.add_entity(self.generate_entity(x, y))

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