from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import config
from models import models

__session = None

load_dotenv()

def init_db():
    global __session
    engine = create_engine(config.DATABASE_URI)
    models.Base.metadata.create_all(engine)
    __session = scoped_session(sessionmaker(bind=engine))


def get_session():
    print("<<<<---- init db session ---->>>>")
    init_db()
    return __session
