from source.vector.vector import Vector

def test_can_instantiate_vector():
    assert Vector
    new_vector = Vector(1, 1)
    assert type(new_vector) is Vector

def test_scalar_multiplication():
    new_vector = Vector(1,1)
    scaled_vector = new_vector.scalar_multiplication(3)
    assert scaled_vector.x == 3
    assert scaled_vector.y == 3

def test_get_coordinate():
    new_vector = Vector(1,2)
    assert new_vector.get_value('x') == 1
    assert new_vector.get_value('y') == 2

def test_add_vector():
    first_vector = Vector(1, 2)
    second_vector = Vector(-2, 4)
    added_vector = first_vector.add_vector(second_vector)
    assert added_vector.x == -1
    assert added_vector.y == 6

def test_dot_product():
    first_vector = Vector(1, 3)
    second_vector = Vector(2, 2)
    assert first_vector.dot_product(second_vector) == 8