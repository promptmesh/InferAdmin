import os
from pathlib import Path

# Create state directory in user's home directory
STATE_DIR = os.path.join(str(Path.home()), ".inferadmin", "state")
