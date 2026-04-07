import os

# default directory of the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# paths to data and exports
DB_PATH = os.path.join(SCRIPT_DIR, "../data/data.db")
JSON_PATH = os.path.join(SCRIPT_DIR, "../docs/data/")

# default database
DEFAULT_DB_NAME = DB_PATH
