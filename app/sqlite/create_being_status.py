from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os
from os.path import join, dirname

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_NAME = os.environ.get("DB_NAME")

engine = create_engine("sqlite:///" + DB_NAME, echo=True)

Base = declarative_base()

class BeingStatus(Base):
    __tablename__ = "being_statuses"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, nullable=False) # 本当はuserの外部キー
    laboratory_id = Column(Integer, nullable=False) # 本当はlaboratoryの外部キー
    status = Column(Boolean, nullable=False)
    time = Column(DateTime(timezone=True), nullable=False, default=func.now())

Base.metadata.create_all(bind=engine)