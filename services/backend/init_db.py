from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from services.backend.config.config import DATABASE_URI
from models.models import Base

__session = None

load_dotenv()


def init_db():
    global __session
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)
    __session = scoped_session(sessionmaker(bind=engine))


def get_session():
    print("<<<<---- init db session ---->>>>")
    init_db()
    return __session
