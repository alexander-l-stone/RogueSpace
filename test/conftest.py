
import pytest

from source.action.action import Action
from source.entity.entity import Entity
from source.area.area import Area
from source.galaxy.galaxy import Galaxy
from source.planet.planet import Planet
from source.system.system import System
from source.action.action_queue import ActionQueue
from source.action.resolution_functions import resolve_no_action
from source.vector.vector import Vector

#TODO: go through tests and see where we are repeating data(for example ActionQueue) and make those fixtures

@pytest.fixture
def action():
    return Action('me', 1, resolve_no_action)

@pytest.fixture
def long_action():
    return Action('long', 2, resolve_no_action)

@pytest.fixture
def entity():
    return Entity(1, 1, '@', (255, 255, 255))

@pytest.fixture
def area():
    return Area()

@pytest.fixture
def area_with_entity():
    area = Area()
    area.add_entity(Entity(1, 1, '@', (30, 60, 150)))
    return area

@pytest.fixture
def planet():
    planet = Planet(4, 5, 'o', (0, 0, 200), 'Test Planet', 'test', None, 5)
    return planet

@pytest.fixture
def system():
    system = System(0, 0, 'O', (255, 0, 0), 'test system', 'test', 50)
    return system

def system_with_planet():
    system = System(0, 0, 'O', (255, 0, 0), 'test system', 'test', 50)
    planet = Planet(4, 5, 'o', (0, 0, 200), 'Test Planet', 'test', None, 5)
    system.add_planet(planet)
    
@pytest.fixture
def action_queue():
    return ActionQueue()

@pytest.fixture
def galaxy():
    return Galaxy()

@pytest.fixture
def vector():
    return Vector(1,1)