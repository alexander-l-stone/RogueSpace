from source.draw.entity.entity import Entity
from random import seed, randint
import math

class Cloud:
    def __init__(self, x, y, char, color, radius, cloud_type, seed, **flags):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.radius = radius
        self.seed = seed
        self.cloud_type = cloud_type
        self.generation_type = 'dense_seeds'
        if ('generation_type' in flags):
            self.generation_type = flags['generation_type']
        self.flags = flags

    def __str__(self) -> str:
        return f"[Cloud]"
    
    def __repr__(self) -> str:
        return f"[Cloud]"
    
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
        elif self.generation_type == 'bubblewalk':
            self.bubblewalk(area)
        elif self.generation_type == 'yinyang_seeds':
            self.yinyang_seeds(area)
        elif self.generation_type == 'dense_seeds':
            self.dense_seeds(area)
        else:
            pass
    
    def random_seeds(self, area):
        seed(self.seed)
        randnumber = randint(1, math.pi*self.radius**2//2)
        area.add_entity(Entity(self.x, self.y, self.char, self.color, self, bg_color=self.color))
        # make i seeds
        for i in range(randnumber):
            xy = self.get_random_point_in_cloud()
            # get all adjacent to seed
            for x in range(xy['x'] - 1, xy['x'] + 2):
                for y in range(xy['y'] - 1, xy['y'] + 2):
                    # probably make cloud
                    d10 = randint(1,10)
                    if d10 <= 7:
                        area.add_entity(Entity(x, y, self.char, self.color, self, bg_color=self.color))

    # do random seeds, but instead of making entities make a dict to cloud level
    # maybe add a negative seed pass for extra texture
    # if cloud level is 1, make light
    # if cloud level is 2, make dark
    def dense_seeds(self, area):
        seed(self.seed)
        randnumber = randint(1, math.pi*self.radius**2//2)
        cloud_dict = {}
        cloud_dict[(self.x,self.y)] = 1
        # make i seeds
        for i in range(randnumber):
            xy = self.get_random_point_in_cloud()
            # get all adjacent to seed
            for x in range(xy['x'] - 1, xy['x'] + 2):
                for y in range(xy['y'] - 1, xy['y'] + 2):
                    # probably make cloud
                    d10 = randint(1,10)
                    if d10 <= 7:
                        if (x,y) in cloud_dict:
                            cloud_dict[(x,y)] += 1
                        else:
                            cloud_dict[(x,y)] = 1
        # make i negative seeds
        for i in range(randnumber//3):
            xy = self.get_random_point_in_cloud()
            # get all adjacent to seed
            for x in range(xy['x'] - 1, xy['x'] + 2):
                for y in range(xy['y'] - 1, xy['y'] + 2):
                    # probably remove cloud
                    d10 = randint(1,10)
                    if d10 <= 7:
                        if (x,y) in area.entity_dict:
                            for entity in area.entity_dict[(x,y)]:
                                if entity.parent == self:
                                    if (x,y) in cloud_dict:
                                        cloud_dict[(x,y)] -= 1
                                    else:
                                        cloud_dict[(x,y)] = -1
        #TODO: Rewrite so we are computing the offset in the walk, rather than computing coord andd subtracting origin        
        for coord,dense in cloud_dict.items():
            if dense == 1 or dense == 2:
                area.add_entity(Entity(coord[0]-self.x, coord[1]-self.y, self.char, self.flags['thin_color'], self, bg_color=self.flags['thin_color']))
            elif dense >= 3:
                area.add_entity(Entity(coord[0] - self.x, coord[1] - self.y, self.char, self.color, self, bg_color=self.color))

    def yinyang_seeds(self, area):
        seed(self.seed)
        randnumber = randint(1, math.pi*self.radius**2//2)
        area.add_entity(Entity(self.x, self.y, self.char, self.color, self))
        # make i seeds
        for i in range(randnumber):
            xy = self.get_random_point_in_cloud()
            # get all adjacent to seed
            for x in range(xy['x'] - 1, xy['x'] + 2):
                for y in range(xy['y'] - 1, xy['y'] + 2):
                    # probably make cloud
                    d10 = randint(1,10)
                    if d10 <= 7:
                        area.add_entity(Entity(x, y, self.char, self.color, self))
        # make i negative seeds
        for i in range(randnumber//4):
            xy = self.get_random_point_in_cloud()
            # get all adjacent to seed
            for x in range(xy['x'] - 1, xy['x'] + 2):
                for y in range(xy['y'] - 1, xy['y'] + 2):
                    # probably remove cloud
                    d10 = randint(1,10)
                    if d10 <= 7:
                        if (x,y) in area.entity_dict:
                            for entity in area.entity_dict[(x,y)]:
                                if entity.parent == self:
                                    area.delete_entity(entity)
    
    def bubblewalk(self, area):
        seed(self.seed)
        randnumber = randint(1, math.pi*self.radius**2//2)
        area.add_entity(Entity(self.x, self.y, self.char, self.color, self))
        # make i root seeds
        for i in range(randnumber):
            xy = self.get_random_point_in_cloud()
            # get all adjacent to seed
            self.seed_cloud(area, xy)
            for j in range(2):
                vec = self.random_dir()
                vec['x'] += xy['x'] * randint(2,4)
                vec['y'] += xy['y'] * randint(2,4)
                self.seed_cloud(area, vec)
                for k in range(2):
                    vec2 = self.random_dir()
                    vec2['x'] += vec['x'] * randint(2,4)
                    vec2['y'] += vec['y'] * randint(2,4)
                    self.seed_cloud(area, vec2)

    def random_dir(self):
        return {'x':randint(-1, 1), 'y':randint(-1, 1)}

    def seed_cloud(self, area, parent_xy):
        for x in range(parent_xy['x'] - 1, parent_xy['x'] + 2):
            for y in range(parent_xy['y'] - 1, parent_xy['y'] + 2):
                # probably make cloud
                    d10 = randint(1,10)
                    if d10 <= 7:
                        area.add_entity(Entity(x, y, self.char, self.color, self))

    def random_bugged_leaves(self, area):
        seed(self.seed)
        randnumber = randint(1, math.pi*self.radius**2//2)
        area.add_entity(Entity(self.x, self.y, self.char, self.color, self))
        x = self.x
        y = self.y
        # generate i branches
        for i in range(randnumber):
            dx = randint(-1, 1)
            dy = randint(-1, 1)
            # don't travel on the z axis
            if not (dx == 0) and not (dy == 0):
                randdist = randint(1, self.radius)
                # random branch length
                for n in range(randdist):
                    # jump far through space to the next leaf
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
                    area.add_entity(Entity(x, y, self.char, self.color, self))

    def random_leaves(self, area):
        seed(self.seed)
        circle_area = math.pi*self.radius**2
        randnumber = randint(circle_area//4, circle_area//2)
        area.add_entity(Entity(self.x, self.y, self.char, self.color, self))
        for i in range(randnumber):
            dx = randint(-1, 1)
            dy = randint(-1, 1)
            x = self.x
            y = self.y
            if not (dx == 0) and not (dy == 0):
                randdist = randint(1, self.radius)
                for n in range(randdist):
                    x += dx
                    y += dy
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
                    area.add_entity(Entity(x, y, self.char, self.color, self))

    def random_walk(self, area):
        seed(self.seed)
        randnumber = randint(1, math.pi*self.radius**2//2)
        x = self.x
        y = self.y
        for i in range(randnumber):
            area.add_entity(Entity(x, y, self.char, self.color, self))
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