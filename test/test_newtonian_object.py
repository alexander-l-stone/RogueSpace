from source.newtonian_object.newtonian_object import NewtonianObject
from source.area.area import Area
from source.entity.entity import Entity
from source.action.move_action import MoveAction

def test_can_instantiate_newtonian_object(area):
    assert NewtonianObject
    new_object = NewtonianObject(0, 0, '@', (0,0,0), area, {'x': 0, 'y': 0})
    assert type(new_object) == NewtonianObject

def test_can_generate_vector_path(area):
    new_object = NewtonianObject(1, 1, '#', (255, 0, 0), area, {'x': 1, 'y': 3})
    new_object.generate_vector_path()
    assert isinstance(area.entity_dict[(1,2)][0], Entity)
    assert isinstance(area.entity_dict[(2,3)][0], Entity)
    assert isinstance(area.entity_dict[(2,4)][0], Entity)
