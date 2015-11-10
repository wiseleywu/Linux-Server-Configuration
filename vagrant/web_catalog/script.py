from sqlalchemy import create_engine, MetaData, Table, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Antibody, Cytotoxin, AntibodyImg, AntibodyLot, CytotoxinImg, CytotoxinLot, Adc, AdcLot, AdcImg
import random
from project import app, fs_store, session, get_picture_url, delete_picture, meta, engine

# attach_picture(Antibody, 5, 'static/images/antibody.png')
# print get_picture_url(Antibody, 5)
# print get_picture_url(1)

# antibody=Table("antibody", meta, autoload=True, autoload_with=engine)
# for x in antibody.columns:
#     print x.type
#
# x=session.query(Antibody).all()
# for y in x:
#     print y.name
maxablot=session.query(AntibodyLot).order_by(desc(AntibodyLot.id)).first().id
maxtoxinlot=session.query(CytotoxinLot).order_by(desc(CytotoxinLot.id)).first().id
print maxablot, maxtoxinlot

test=session.query(AntibodyLot).filter_by(id=20).one()
print test.user_id
