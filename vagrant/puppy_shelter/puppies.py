from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()

adoption_id = Table('adoption_id', Base.metadata,
                Column('puppy_id', Integer, ForeignKey('puppy.id')),
                Column('adopter_id', Integer, ForeignKey('adopter.id'))
                )

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    capacity = Column(Integer)
    occupancy = Column(Integer)

class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))

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
    adopter = relationship(Adopter, secondary=adoption_id, backref='puppy')

class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    special = Column(String)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship(Puppy, uselist=False, backref='profile')

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
