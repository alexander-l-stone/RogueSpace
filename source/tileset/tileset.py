class Tileset:
    def __init__(self, tiles:dict):
        """
        A class that containes a tileset and its tiles.

        Args:
            tiles (dict): A dictionary of tiles. The dictionary should be of the form
            {
                1: TILE,
                2: OTHER_TILE,
            }
            etc ...
        """
        self.tiles = tiles
    
    def add_tile(self, tile) -> None:
        """
        Adds a tile to the tileset at the lowest unused positive integer.

        Args:
            tile (any): [description]
        """
        i = 0
        while True:
            if i not in self.tiles:
                self.tiles[i] = tile
                return
            else:
                i += 1
    
    def add_tile_with_key(self, key:int, tile) -> None:
        """
        Adds a key to the tileset with key of key. Will overwrite anything currently there

        Args:
            key (int): The key associated with the added tile
            tile (any): The tile to be added
        """
        self.tiles[key] = tile
    
    def get_tile(self, key:int):
        """
        Gets tile at key. Raises KeyError if it does not exist.

        Args:
            key (int): Key for the tile to be grabbed.
        """
        return self.tiles[key]