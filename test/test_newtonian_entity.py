from source.ship.ship_components.newtonian_mover import NewtonianMover
from source.draw.entity.entity import Entity
from source.action.action import Action
from source.action.resolution_functions import resolve_no_action
from source.ship.ship import Ship
from source.vector.vector import Vector

def test_can_instantiate_newtonian_entity(area):
    assert NewtonianMover
    new_object = NewtonianMover(None, {'x': 0, 'y': 0})
    assert type(new_object) == NewtonianMover

#TODO: Once vector path is in a more final state, make this test code more restrictive
def test_can_generate_vector_path(area):
    new_object_positive = Ship('?', (255, 0, 0), curr_area = area)
    new_object_positive.engine.vector = Vector(1,3)
    new_object_positive.engine.generate_vector_path()
    assert len(area.entity_dict) >= 4

def test_thrust(area):
    new_object = Ship('?', (255, 0, 0), curr_area = area)
    new_object.engine.thrust(-1, -1)
    assert new_object.engine.vector.x == -1
    assert new_object.engine.vector.y == -1
    new_object.engine.thrust(0, 17)
    assert new_object.engine.vector.x == -1
    assert new_object.engine.vector.y == 16

def test_move(area, action_queue):
    new_object = Ship('?', (255, 0, 0), curr_area=area)
    new_object.engine.vector = Vector(1,3)
    vector_move_actions = new_object.engine.generate_move_actions(0,1)
    for action in vector_move_actions:
        action_queue.push(action)
        action_queue.push(Action(new_object, 1, resolve_no_action))
    action_queue.resolve_actions(1)
    assert new_object.get_x() == 1
    assert new_object.get_y() == 3
