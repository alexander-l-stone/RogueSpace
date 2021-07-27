from source.entity.entity import Entity
from source.action.move_action import MoveAction
from source.helper_functions.is_negative import is_negative

class NewtonianEntity(Entity):
    def __init__(self, x:int, y:int, char:str, color:tuple, area, vector:dict, **flags):
        """Constructor for the NewtonianObject

        Args:
            x (int): X coordinate of the object
            y (int): Y coordinate of the object
            char (str): Character to display on the screen.
            color (tuple): Color of the character
            area (Area): Area the object is in
            vector (dict): Vector the object is on. Will be of the form {x: int, y: int}
        """
        Entity.__init__(self, x, y, char, color, flags)
        self.curr_area = area
        self.vector = vector
        self.vector_entities = [] #A list of entities that compose this objects vector path

    def generate_vector_path(self) -> None:
        """Create and add to the area the entities that show the path this object will take.
        """
        #Delete the previous Entities
        for entity in self.vector_entities:
            self.curr_area.delete_entity_at_coordinates(entity, entity.x, entity.y)
        try:
            #Figure out wich of x or y is greater and store the value of the lesser divided by the greater. This is guaranteed to not be more than 1
            if abs(self.vector['x']) > abs(self.vector['y']):
                normalized_dict = {'greater': 'x', 'lesser': 'y', 'low/great': abs(self.vector['y']/self.vector['x'])}
            else:
                normalized_dict = {'greater': 'y', 'lesser': 'x', 'low/great': abs(self.vector['x']/self.vector['y'])}
        except ZeroDivisionError:
            return
        coordinate_dict = {'x': 0, 'y': 0}
        for i in range(0, abs(self.vector[normalized_dict['greater']])):
            coordinate_dict[normalized_dict['greater']] += 1 * is_negative(self.vector[normalized_dict['greater']])
            coordinate_dict[normalized_dict['lesser']] += normalized_dict['low/great'] * is_negative(self.vector[normalized_dict['lesser']])
            vector_entity = Entity(self.x + round(coordinate_dict['x']), self.y + round(coordinate_dict['y']), '.', self.color)
            self.curr_area.add_entity(vector_entity)
            self.vector_entities.append(vector_entity)
    
    def generate_move_actions(self, time) -> list:
        """
            Generates a list of MoveActions based upon this objects vector.

            time [int] - The time these move actions should be generated at.

            This should never be called until all the previous move actions from it have been resolved
        """
        move_actions = []
        try:
            if abs(self.vector['x']) > abs(self.vector['y']):
                normalized_dict = {'greater': 'x', 'lesser': 'y', 'low/great': abs(self.vector['y']/self.vector['x'])}
            else:
                normalized_dict = {'greater': 'y', 'lesser': 'x', 'low/great': abs(self.vector['x']/self.vector['y'])}
        except ZeroDivisionError:
            return move_actions
        coordinate_dict = {'x': 0, 'y': 0}
        coordinate_dict[normalized_dict['greater']] = 1 * is_negative(self.vector[normalized_dict['greater']])
        if 'is_player' in self.flags:
            is_player = True
        else:
            is_player = False
        for i in range(0, abs(self.vector[normalized_dict['greater']])):
            coordinate_dict[normalized_dict['lesser']] += normalized_dict['low/great'] * is_negative(self.vector[normalized_dict['lesser']])
            move_actions.append(MoveAction(self, time, round(coordinate_dict['x']), round(coordinate_dict['y']), self.curr_area, is_player=is_player))
            if round(coordinate_dict[normalized_dict['lesser']]) >= 1:
                coordinate_dict[normalized_dict['lesser']] = 0
        return move_actions

    def thrust(self, dx:int, dy:int) -> None:
        """Add values to this object vector.

        Args:
            dx (int): The x part of the vector to add
            dy (int): The y part of the vector to add
        """
        self.vector['x'] += dx
        self.vector['y'] += dy
        self.generate_vector_path()