from source.galaxy.galaxy import Galaxy

def test_can_instantiate_galaxy():
    assert Galaxy
    new_galaxy = Galaxy()
    assert isinstance(new_galaxy, Galaxy)

def test_galaxy_exploration(galaxy):
    galaxy.explored_dict = {(0,0): True, (1,0): True, (-1,0): True}
    assert galaxy.check_if_coordinate_is_explored(1, 499) == True
    assert galaxy.check_if_coordinate_is_explored(1, -1) == False