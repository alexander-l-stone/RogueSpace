import math
from source.system.system import System
from random import seed, randint

class GalaxyGenerator:
    def __init__(self):
        self.generator_queue = []
    
    def resolve_generator_queue(self, galaxy):
        for item in self.generator_queue:
            if item['type'] == 'solar_system':
                if ((item['x'], item['y']) not in galaxy.system_dict):
                    galaxy.system_dict[(item['x'], item['y'])] = self.generate_solar_system(item['x'], item['y'])
            if item['type'] == 'cluster':
                self.generate_cluster(item['x'], item['y'], item['radius'])

    def generate_sector(self, x, y):
        

    def generate_cluster(self, x, y, radius):
        cluster_area = int(math.pi*radius**2)
        num_system_to_generate = randint(1, cluster_area//4)
        for i in range(0, num_system_to_generate):
            randx = randint(x - radius, x + radius)
            randy = randint(y - radius, y + radius)
            self.generator_queue.append({'type': 'solar_system', 'x': randx, 'y': randy})

    def generate_solar_system(self, x, y):
        return System(x, y, 'O', (0, 0, 255), f"Placeholder: {x}, {y}", "placeholder", 10)