from source.newtonian_object.newtonian_object import NewtonianObject
from source.area.area import Area
from source.action.move_action import MoveAction

def test_can_instantiate_newtonian_object(area):
    assert NewtonianObject
    new_object = NewtonianObject(0, 0, '@', (0,0,0), area, {'dx': 0, 'dy': 0})
    assert type(new_object) == NewtonianObject

def test_can_generate_vector_path(area):
    new_object = NewtonianObject(1, 1, '#', (255, 0, 0), area, {'dx': 1, 'dy': 3})
    new_object.generate_vector_path()
    