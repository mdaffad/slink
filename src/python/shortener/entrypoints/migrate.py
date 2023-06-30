# Wrapper to access alembic with pex binary or pants run
import sys

from alembic.config import main

if __name__ == "__main__":
    # exclude path of binary pex file
    main(argv=sys.argv[1:])
