from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Antibody, Cytotoxin, AntibodyImg, AntibodyLot, CytotoxinImg, CytotoxinLot, ADC, ADCLot
import random

engine=create_engine('sqlite:///biologicscatalog.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()

print session.query(Antibody).count()
