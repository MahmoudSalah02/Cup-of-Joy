from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config.config import DATABASE_URI
from models.models import Base

load_dotenv()

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
session = scoped_session(sessionmaker(bind=engine))
