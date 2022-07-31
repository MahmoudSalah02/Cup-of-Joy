from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.models import Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = f"postgresql+psycopg2://postgres:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:5433/{os.getenv('DBNAME')}"
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
session = scoped_session(sessionmaker(bind=engine))

