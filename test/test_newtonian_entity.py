from source.draw.entity.newtonian_entity import NewtonianMover
from source.draw.entity.entity import Entity
from source.action.action import Action
from source.action.resolution_functions import resolve_no_action
from source.ship.ship import Ship
from source.vector.vector import Vector

def test_can_instantiate_newtonian_entity(area):
    assert NewtonianMover
    new_object = NewtonianMover(None, {'x': 0, 'y': 0})
    assert type(new_object) == NewtonianMover

def test_can_generate_vector_path(area):
    new_object_positive = Ship('?', (255, 0, 0))
    new_object_positive.engine.vector = Vector(1,3)
    area.add_entity(new_object_positive)
    new_object_positive.engine.generate_vector_path()
    assert isinstance(area.entity_dict[(1,2)][0], Entity)
    assert isinstance(area.entity_dict[(2,3)][0], Entity)
    assert isinstance(area.entity_dict[(2,4)][0], Entity)
    new_object_negative = Ship('?', (255, 0, 0))
    new_object_negative.engine.vector = Vector(-1, -3)
    area.add_entity(new_object_negative)
    new_object_negative.engine.generate_vector_path()
    assert isinstance(area.entity_dict[(-1,-2)][0], Entity)
    assert isinstance(area.entity_dict[(-2,-3)][0], Entity)
    assert isinstance(area.entity_dict[(-2,-4)][0], Entity)

def test_thrust(area):
    new_object = Ship('?', (255, 0, 0))
    new_object.engine.thrust(-1, -1)
    new_object.engine.generate_move_actions()
    assert isinstance(area.entity_dict[(-1,-1)][0], Entity)

def test_move(area, action_queue):
    new_object = Ship('?', (255, 0, 0))
    new_object.engine.vector = Vector(1,3)
    vector_move_actions = new_object.engine.generate_move_actions(1)
    for action in vector_move_actions:
        action_queue.push(action)
        action_queue.push(Action(new_object, 1, resolve_no_action))
    action_queue.resolve_actions(1)
    assert new_object.x == 2
    assert new_object.y == 4
