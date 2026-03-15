"""Allow running as python -m cursor_hub."""
import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
