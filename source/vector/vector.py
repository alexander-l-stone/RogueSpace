import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_value(self, coordinate:str) -> int:
        if coordinate == 'x':
            return self.x
        elif coordinate == 'y':
            return self.y
        else:
            raise ValueError

    def scalar_multiplication(self, scalar:float):
        return Vector(self.x * scalar, self.y * scalar)
    
    def add_vector(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)
    
    def dot_product(self, vector) -> int:
        return self.x * vector.x + self.y * vector.y

    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)