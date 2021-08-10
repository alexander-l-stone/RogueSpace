from source.tileset.tileset import Tileset

def test_can_instantiate_tilset():
    assert Tileset
    new_tileset = Tileset({0: '#'})
    assert type(new_tileset) is Tileset

def test_can_get_tile_from_tileset(tileset):
    assert tileset.get_tile(0) == tileset.tiles[0]

def test_get_tileset_not_in_tileset_raises_key_error(tileset):
    error = False
    try:
        tileset.get_tile(1)
    except KeyError:
        error = True
    assert error

def test_can_add_tile_to_tileset(tileset):
    tileset.add_tile('^')
    assert tileset.get_tile(1) == '^'

def test_can_add_tile_to_tileset_at_key(tileset):
    tileset.add_tile_with_key(2, '@')
    assert tileset.get_tile(2) == '@'

def test_can_overwrite_tile_in_tileset_at_key(tileset):
    assert tileset.get_tile(0) == '#'
    tileset.add_tile_with_key(0, '$')
    assert tileset.get_tile(0) == '$'