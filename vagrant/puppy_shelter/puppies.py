from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))

# class Profile(Base):
#     __tablename__ = 'profile'
#     id = Column(Integer, ForeignKey('puppy.id'))
#     puppy = relationship(Puppy)
#     description = Column(String)
#     special = Column(String)

# class Adopter(Base):
#     __tablename__ = 'adopter'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#     gender = Column(String(6), nullable = False)
#     dateOfBirth = Column(Date)
#     address = Column(String(250))
#     city = Column(String(80))
#     state = Column(String(20))
#     zipCode = Column(String(10))
#     puppy_id = Column(Integer, ForeignKey('puppy.id'))
#     puppy = relationship(Puppy)

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
