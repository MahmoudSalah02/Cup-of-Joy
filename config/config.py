from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from pathlib import Path

ROLE_MAPPING = {
    "/shop": ["cashier", "manager"],
    "/operation": ["manager"],
}

# ROOT_PATH = Path(__file__).parent.parent
# sql_url = "sqlite:///" + str(ROOT_PATH).replace("src", "").replace("\\", "\\\\") + "\\\\cafe.db"
# engine = create_engine(sql_url)
#
# # the scoped_session() function is provided which produces a thread-managed registry of Session objects
# session = scoped_session(sessionmaker(bind=engine))

# TODO: write config in this format
# import os
#
# from dotenv import load_dotenv, find_dotenv
#
# load_dotenv(find_dotenv())
#
# class Development(object):
#     """
#     Development environment configuration
#     """
#     DEBUG = True
#     TESTING = False
#     JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
#
# app_config = {
#     'development': Development,
#     'production': Production,
# }