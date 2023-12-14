from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from os.path import join, dirname

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_NAME = os.environ.get("DB_NAME")

engine = create_engine("sqlite:///" + DB_NAME, echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    laboratory_id = Column(Integer, nullable=False) # 本当はlaboratoryの外部キー
    name = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)