from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from pathlib import Path

ROLE_MAPPING = {
    "/shop": ["cashier", "manager"],
    "/operation": ["manager"],
}

ROOT_PATH = Path(__file__).parent.parent
sql_url = "sqlite:///" + str(ROOT_PATH).replace("src", "").replace("\\", "\\\\") + "\\\\cafe.db"
engine = create_engine(sql_url)

# the scoped_session() function is provided which produces a thread-managed registry of Session objects
session = scoped_session(sessionmaker(bind=engine))
