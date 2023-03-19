from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config


DB_USER = config('POSTGRES_USER')
DB_PASSWORD = config('POSTGRES_PASSWORD')

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/parser", echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    link = Column(String(255))
    location = Column(String(255))
    time = Column(String(255))


class AlterNews(Base):
    __tablename__ = "alter_news"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    location = Column(String(255))
    link = Column(String(255))


class Disaster(Base):
    __tablename__ = "disasters"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    disaster_type = Column(String(255))
    affected_countries = Column(String(255))

Base.metadata.create_all(engine)
