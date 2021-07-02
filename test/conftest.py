
import pytest

from source.action.action import Action
from source.entity.entity import Entity
from source.area.area import Area
from source.planet.planet import Planet
from source.system.system import System

#TODO: go through tests and see where we are repeating data(for example ActionQueue) and make those fixtures

@pytest.fixture
def action():
    return Action('me', 1)

@pytest.fixture
def long_action():
    return Action('long', 2)

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