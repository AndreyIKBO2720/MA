from sqlalchemy import create_engine, Column, String, Time, Integer, Date, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Purchase(Base):
    __tablename__ = 'purchase_bashkirov'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    text = Column(String, nullable=False)
    price = Column(Float, nullable=False)
