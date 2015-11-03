from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Antibody, Cytotoxin, AntibodyImg, AntibodyLot, CytotoxinImg, CytotoxinLot, ADC, ADCLot
import random
from project import app, fs_store, session, attach_picture, get_picture_url

# attach_picture(Antibody, 5, 'static/images/i9V4DKH.jpg')
# print get_picture_url(Antibody, 5)
#
# def delete_picture(table, item_id):
#     item=session.query(table).filter_by(id=item_id).one()
#     with store_context(fs_store):
#         fs_store.delete(item.picture.original)
#         session.commit()
#     print "image deleted"
#
# print delete_picture(Antibody, 5)
