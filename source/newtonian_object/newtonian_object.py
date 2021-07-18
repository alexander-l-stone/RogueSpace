from source.entity.entity import Entity

class NewtonianObject:
    def __init__(self, x:int, y:int, char:str, color:tuple, area, vector:dict, **flags):
        """Constructor for the NewtonianObject

        Args:
            x (int): X coordinate of the object
            y (int): Y coordinate of the object
            char (str): Character to display on the screen.
            color (tuple): Color of the character
            area (Area): Area the object is in
            vector (dict): Vector the object is on. Will be of the form {dx: int, dy: int}
        """
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.area = area
        self.vector = vector
        self.flags = flags
        self.vector_entities = [] #A list of entities that compose this objects vector path

    def generate_vector_path(self) -> None:
        """Create and add to the area the entities that show the path this object will take.
        """
        #Delete the previous Entities
        for entity in self.vector_entities:
            self.area.delete_entity_at_coordinates(entity, entity.x, entity.y)
        #Figure out wich of x or y is greater and store the value of the lesser divided by the greater. This is guaranteed to not be more than 1
        if self.vector['x'] > self.vector['y']:
            normalized_dict = {'greater': 'x', 'lesser': 'y', 'low/great': self.vector_entities['y']/self.vector_entities['x']}
        else:
            normalized_dict = {'greater': 'y', 'lesser': 'x', 'low/great': self.vector_entities['x']/self.vector_entities['y']}
        coordinate_dict = {'dx': 0, 'dy': 0}
        for i in range(0, self.vector_entities[normalized_dict['greater']]):
            coordinate_dict[normalized_dict['greater']] += 1
            coordinate_dict[normalized_dict['lesser']] += normalized_dict['low/great']
            vector_entity = Entity(self.x + round(coordinate_dict['dx']), self.y + round(coordinate_dict['dy']), '.', self.color)
            self.area.add_entity(vector_entity)
            self.vector_entities.append(vector_entity)
    
    def generate_object_entity(self) -> Entity:
        """Generate the Entity that represents this object

        Returns:
            Entity: The entity that represents this object
        """
        return Entity(self.x, self.y, self.char, self.color)

    def thrust(self, dx:int, dy:int) -> None:
        """Add values to this object vector.

        Args:
            dx (int): The x part of the vector to add
            dy (int): The y part of the vector to add
        """
        self.vector['dx'] += dx
        self.vector['dy'] += dy