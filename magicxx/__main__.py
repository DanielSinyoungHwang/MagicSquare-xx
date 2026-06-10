"""python -m magicxx verify"""

import sys

from magicxx.cli import main

if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv and argv[0] == "verify":
        argv = argv[1:]
    raise SystemExit(main(argv))
