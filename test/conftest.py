
import pytest

from source.action.action import Action
from source.entity.entity import Entity
from source.area.area import Area

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