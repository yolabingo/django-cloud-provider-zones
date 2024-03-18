from pathlib import Path

CLOUD_PROVIDERS = [
    "aws",
    "gcp",
]

PROJECT_ROOT_DIR = Path(__file__).parent.parent
APP_NAME = "django_cloud_provider_zones"
APP_DIR = PROJECT_ROOT_DIR / "src" / APP_NAME
REGION_DATA_DIR = PROJECT_ROOT_DIR / "region_data"
UNPARSED_GCLOUD_JSON = REGION_DATA_DIR / "unparsed_gcloud_output.json"

FIXTURES_DIR = APP_DIR / "fixtures"
TEST_DB_PATH = APP_DIR / "test_db.sqlite3"
