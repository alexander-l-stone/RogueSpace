from source.draw.entity.entity import Entity
from source.action.action import Action
from source.action.resolution_functions import resolve_move_action
from source.helper_functions.is_negative import is_negative
from source.vector.vector import Vector
from source.draw.area.area import Area

#TODO Seperate Newtonian Movement from Entity. Should either be on ship, or more likely, a seperate set of functions that anything with thrust can use.

class NewtonianMover:
    def __init__(self, parent, vector:dict, **flags):
        self.parent = parent
        self.vector = Vector(vector['x'], vector['y'])
        self.flags = flags

    def generate_vector_path(self) -> None:
        """Create and add to the area the entities that show the path this object will take.
        """
        update_rate = 2 * self.vector.magnitude()

    def update_path(self):
        pass

    def generate_move_actions(self, time, span) -> list:
        """
            Generates a list of movement Actions based upon this objects vector.
            Will generate movements with the first occuring immediately, andd the rest occuring in 1/update_rate intervals
            update_rate is currently set to make all movements .5 tiles in length

            time [int] - The time these movements start.
            span [int] - The amount of time to generate movements over

            This should never be called until all the previous move actions from it have been resolved
        """
        if(self.vector.magnitude() == 0.0):
            return []
        
        move_actions = []
        local_time = float(time)
        update_rate = 2 * self.vector.magnitude()
        x_increment = self.vector.x / update_rate 
        y_increment = self.vector.y / update_rate
        #TODO: Is_player is currently 'true'. fix this. 
        while(local_time < time + span):
            move_actions.append(Action(self.parent, local_time, resolve_move_action, dx=x_increment, dy=y_increment, area=self.parent.entity_repr.curr_area, is_player=True))
            local_time += 1 / update_rate
        return move_actions

    def thrust(self, dx:int, dy:int) -> None:
        #May or may not wish to exist
        """Add values to this object vector.

        Args:
            dx (int): The x part of the vector to add
            dy (int): The y part of the vector to add
        """
        self.vector.x += dx
        self.vector.y += dy
        self.generate_vector_path()