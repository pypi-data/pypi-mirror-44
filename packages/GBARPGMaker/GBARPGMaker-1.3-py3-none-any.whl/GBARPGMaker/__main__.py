import argparse
import sys

from GBARPGMaker.GBARPGMaker import GBARPGMaker


def main():
    parser = argparse.ArgumentParser(description='Command line program to help with development of GBA games.')

    parser.add_argument("command", choices=["make", "genmain", "inter"])

    args = parser.parse_args()

    sys.path.append("./")

    try:
        import config
    except ModuleNotFoundError:
        print("There is no config.py file in your current directory")
        return

    if args.command == "make":
        grm = GBARPGMaker(config)
        grm.make_game()
    elif args.command == "genmain":
        grm = GBARPGMaker(config)
        grm.generate_main()
    elif args.command == "inter":
        grm = GBARPGMaker(config)
        m = grm.maps[list(grm.maps.keys())[0]]
        s = grm.sprite_graphics[list(grm.sprite_graphics.keys())[0]]
        __import__('IPython').embed()


if __name__ == "__main__":
    main()

