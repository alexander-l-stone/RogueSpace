from source.entity.entity import Entity
from random import seed, randint
import math

class Cloud:
    def __init__(self, x, y, char, color, radius, seed, **flags):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.radius = radius
        self.seed = seed
        self.generation_type = 'random_seeds'
        if ('generation_type' in flags):
            self.generation_type = flags['generation_type']
        self.flags = flags
    
    def get_random_point_in_cloud(self):
        randTheta = randint(0, 360) * math.pi/180
        randradius = randint(0, self.radius)
        return {'x': int(randradius * math.cos(randTheta)) + self.x, 'y': int(randradius * math.sin(randTheta)) + self.y}

    def generate_entities(self, area):
        if self.generation_type == 'random_walk':
            self.random_walk(area)
        elif self.generation_type == 'random_leaves':
            self.random_leaves(area)
        elif self.generation_type == 'bugged_leaves':
            self.random_bugged_leaves(area)
        elif self.generation_type == 'random_seeds':
            self.random_seeds(area)
        else:
            pass
    
    def random_seeds(self, area):
        seed(self.seed)
        randnumber = randint(1, math.pi*self.radius**2//2)
        area.add_entity(Entity(self.x, self.y, self.char, self.color))
        for i in range(randnumber):
            xy = self.get_random_point_in_cloud()
            for x in range(xy['x'] - 1, xy['x'] + 2):
                for y in range(xy['y'] - 1, xy['y'] + 2):
                    d10 = randint(1,10)
                    if d10 < 8:
                        area.add_entity(Entity(x, y, self.char, self.color))

    def random_bugged_leaves(self, area):
        randnumber = randint(1, math.pi*self.radius**2//2)
        area.add_entity(Entity(self.x, self.y, self.char, self.color))
        x = self.x
        y = self.y
        for i in range(randnumber):
            dx = randint(-1, 1)
            dy = randint(-1, 1)
            if not (dx == 0) and not (dy == 0):
                randdist = randint(1, self.radius)
                for n in range(randdist):
                    x = x + n * dx
                    y = y + n * dy
                    dx = dx + randint(-1, 1)
                    dy = dy + randint(-1, 1)
                    if dx < -1:
                        dx = -1
                    elif dx > 1:
                        dx = 1
                    if dy < -1:
                        dy = -1
                    elif dy > 1:
                        dy = 1
                    area.add_entity(Entity(x, y, self.char, self.color))

    def random_leaves(self, area):
        randnumber = randint(1, math.pi*self.radius**2//2)
        area.add_entity(Entity(self.x, self.y, self.char, self.color))
        for i in range(randnumber):
            dx = randint(-1, 1)
            dy = randint(-1, 1)
            x = self.x
            y = self.y
            if not (dx == 0) and not (dy == 0):
                randdist = randint(1, self.radius)
                for n in range(randdist):
                    x = x + n * dx
                    y = y + n * dy
                    dx = dx + randint(-1, 1)
                    dy = dy + randint(-1, 1)
                    if dx < -1:
                        dx = -1
                    elif dx > 1:
                        dx = 1
                    if dy < -1:
                        dy = -1
                    elif dy > 1:
                        dy = 1
                    area.add_entity(Entity(x, y, self.char, self.color))

    def random_walk(self, area):
        randnumber = randint(1, math.pi*self.radius**2//2)
        x = self.x
        y = self.y
        for i in range(randnumber):
            area.add_entity(Entity(x, y, self.char, self.color))
            d2 = randint(1, 2)
            d22 = randint(1, 2)
            #This is the second d2
            if d2 == 1:
                if d22 == 1:
                    dx = 1
                    dy = 0
                else:
                    dx = -1
                    dy = 0
            else:
                if d22 == 1:
                    dx = 0
                    dy = 1
                else:
                    dx = 0
                    dy = -1
            x += dx
            y += dy