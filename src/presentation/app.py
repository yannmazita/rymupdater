import sys

from src.application.services import RYMupdater
from src.presentation.cli import Cli


def main() -> int:
    cli: Cli = Cli(sys.argv[1])
    cli.displayCurrentFilePath()
    return 0


if __name__ == "__main__":
    sys.exit(main())
