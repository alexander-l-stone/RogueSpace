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
