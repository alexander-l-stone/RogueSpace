
import pytest

from source.action.action import Action

@pytest.fixture
def action():
    return Action('me', 1)

@pytest.fixture
def long_action():
    return Action('long', 2)