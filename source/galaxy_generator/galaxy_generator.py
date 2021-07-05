import math
from source.system.system import System

class GalaxyGenerator:
    def __init__(self):
        pass
    
    def generate_solar_system(self, x, y):
        return System(x, y, 'O', (0, 0, 255), f"Placeholder: {x}, {y}", "placeholder", 10)