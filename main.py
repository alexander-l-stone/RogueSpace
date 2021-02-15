import tcod
import argparse

from source.game import Game

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", required=False, action='store_true')
    config = vars(ap.parse_args())
    
    game = Game(config)
    
    game.game_loop()