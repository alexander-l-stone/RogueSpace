import tcod
import tcod.event
import argparse

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", required=False, action='store_true')
    config = vars(ap.parse_args())