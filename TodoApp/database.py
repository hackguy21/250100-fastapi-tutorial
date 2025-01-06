from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# create location on db on our fastapi application

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {'check_same_thread':False})
# define connection with db
# sql allow only one thread to communicate with
# preventing any kind of accident with different request

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


