import os
from pathlib import Path

# Create state directory in user's home directory
# When running in Docker, this will use the container's home directory
# which will persist as long as volumes are configured correctly
STATE_DIR = os.path.join(str(Path.home()), ".inferadmin", "state")
