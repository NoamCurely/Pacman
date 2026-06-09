"""Entry point: parse the config file and launch the game."""
import sys

from src.parsing import Parsing, ParsingError, Config
from src.launch import Launch


def main() -> None:
    """Parse argv, load the config and start the game."""
    if len(sys.argv) != 2:
        print("Your program must be launched: python3 pac-man.py config.json")
        sys.exit(1)
    try:
        config = Parsing(sys.argv[1]).open_file()
    except ParsingError as e:
        print(f"Warning: {e} — using default config", file=sys.stderr)
        config = Config()
    Launch(config).menu()


if __name__ == "__main__":
    main()
