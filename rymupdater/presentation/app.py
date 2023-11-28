import sys
import argparse

from .cli import Cli
from .gui import startGUI


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Use rateyourmusic.com to update id3 tags."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-cli", "-c", nargs=1)
    group.add_argument("-gui", "-g", action="store_true")
    args = parser.parse_args()

    if not args.gui and not args.cli:
        startGUI()
    elif args.cli:
        cli: Cli = Cli(args.cli[0])
        cli.displayCurrentFilePath()
    else:
        startGUI()
    return 0


if __name__ == "__main__":
    sys.exit(main())
