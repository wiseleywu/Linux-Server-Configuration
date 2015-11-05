from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Antibody, Cytotoxin, AntibodyImg, AntibodyLot, CytotoxinImg, CytotoxinLot, ADC, ADCLot
import random
from project import app, fs_store, session, attach_picture, get_picture_url, delete_picture

# attach_picture(Antibody, 5, 'static/images/antibody.png')
# print get_picture_url(Antibody, 5)
print get_picture_url(1)
