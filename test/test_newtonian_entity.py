from source.entity.newtonian_entity import NewtonianEntity
from source.entity.entity import Entity
from source.action.action import Action
from source.action.resolution_functions import resolve_no_action

def test_can_instantiate_newtonian_entity(area):
    assert NewtonianEntity
    new_object = NewtonianEntity(0, 0, '@', (0,0,0), None, area, {'x': 0, 'y': 0}, None)
    assert type(new_object) == NewtonianEntity

def test_can_generate_vector_path(area):
    new_object_positive = NewtonianEntity(1, 1, '#', (255, 0, 0), None, area, {'x': 1, 'y': 3})
    area.add_entity(new_object_positive)
    new_object_positive.generate_vector_path()
    assert isinstance(area.entity_dict[(1,2)][0], Entity)
    assert isinstance(area.entity_dict[(2,3)][0], Entity)
    assert isinstance(area.entity_dict[(2,4)][0], Entity)
    new_object_negative = NewtonianEntity(-1, -1, '#', (255, 0, 0), None, area, {'x': -1, 'y': -3})
    area.add_entity(new_object_negative)
    new_object_negative.generate_vector_path()
    assert isinstance(area.entity_dict[(-1,-2)][0], Entity)
    assert isinstance(area.entity_dict[(-2,-3)][0], Entity)
    assert isinstance(area.entity_dict[(-2,-4)][0], Entity)

def test_thrust(area):
    new_object = NewtonianEntity(1, 1, '#', (255, 0, 0), None, area, {'x': 1, 'y': 3})
    new_object.generate_vector_path()
    assert isinstance(area.entity_dict[(1,2)][0], Entity)
    assert isinstance(area.entity_dict[(2,3)][0], Entity)
    assert isinstance(area.entity_dict[(2,4)][0], Entity)
    new_object.thrust(-1, -1)
    assert isinstance(area.entity_dict[(1,2)][0], Entity)
    assert isinstance(area.entity_dict[(1,3)][0], Entity)

def test_move(area, action_queue):
    new_object = NewtonianEntity(1, 1, '#', (255, 0, 0), None, area, {'x': 1, 'y': 3})
    new_object.generate_vector_path()
    vector_move_actions = new_object.generate_move_actions(1)
    for action in vector_move_actions:
        action_queue.push(action)
        action_queue.push(Action(new_object, 1, resolve_no_action))
    action_queue.resolve_actions(1)
    assert new_object.x == 2
    assert new_object.y == 4
