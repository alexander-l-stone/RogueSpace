from source.system.system import System
from source.draw.entity.entity import Entity
from source.draw.area.area import Area
from source.action.action import Action
from source.action.resolution_functions import resolve_move_action

def test_can_instantiate_system():
    """
    Test that system imports properly and its constructor works.
    """
    assert System
    system = System(1, 1, 'o', (255, 0, 0), 'test', 'test', None, 5, 0, 0, 0, 0)
    assert type(system) is System

def test_can_generate_system_area(system):
    assert isinstance(system.generate_area(), Area)

def test_sector_level_collide(system, action_queue):
    area = Area()
    area.add_entity(system.generate_star_entity())
    moving_entity = Entity(-1, 0, 'e', (255,0,0), None)
    area.add_entity(moving_entity)
    move_action = Action(moving_entity, 1, resolve_move_action, dx=1, dy=0, area=area)
    action_queue.push(move_action)
    result = action_queue.resolve_actions(1)
    assert result == [{
        'type': 'enter',
        'entering_entity': moving_entity,
        'target_entity': system
    }]