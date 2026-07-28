import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "data.db"
JSON_OUTPUT_PATH = BASE_DIR / "docs" / "data"
TEST_JSON_OUTPUT_PATH = BASE_DIR / "tests" / "data"

IS_TEST = os.getenv("SDS_ENV") == "test"

EXPORT_PATH = TEST_JSON_OUTPUT_PATH if IS_TEST else JSON_OUTPUT_PATH
