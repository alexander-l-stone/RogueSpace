from source.area.area import Area

class Galaxy:
    def __init__(self):
        self.explored_dict = {}
        self.system_dict = {}
        self.sector_size:int = 200
    
    def check_if_coordinate_is_explored(self, x, y) -> bool:
        return (int(x/200), int(y/200)) in self.explored_dict
    
    def g