import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
TESTING = False
PRIVATE_KEY_PATH = "data/jwt-key"
PUBLIC_KEY_PATH = "data/jwt-key.pub"
ALGORITHM = "RS256"
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')
DATABASE_URI = f"postgresql+psycopg2://postgres:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ROLE_MAPPING = {
    "/shop": ["cashier", "manager"],
    "/operation": ["manager"],
}
TOKEN_EXPIRE_HOURS = os.getenv("TOKEN_EXPIRE_HOURS", 1)


