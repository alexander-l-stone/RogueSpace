from _pytest.monkeypatch import resolve
from source.system.system import System
from source.entity.entity import Entity
from source.area.area import Area
from source.action.move_action import MoveAction

def test_can_instantiate_system():
    """
    Test that system imports properly and its constructor works.
    """
    assert System
    system = System(1, 1, 'o', (255, 0, 0), 'test', 'test', None, 5)
    assert type(system) is System

def test_can_generate_system_area(system):
    assert isinstance(system.generate_area(), Area)

def test_sector_level_collide(system, action_queue):
    area = Area()
    area.add_entity(system.generate_star_entity())
    moving_entity = Entity(-1, 0, 'e', (255,0,0))
    area.add_entity(moving_entity)
    move_action = MoveAction(moving_entity, 1, 1, 0, area)
    action_queue.push(move_action)
    result = action_queue.resolve_actions(1)
    assert result == [{
        'type': 'enter',
        'entering_entity': moving_entity,
        'target_entity': system
    }]