from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Antibody, Cytotoxin, AntibodyImg, AntibodyLot, CytotoxinImg, CytotoxinLot, ADC, ADCLot
import random

engine=create_engine('sqlite:///biologicscatalog.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()

def antibodylot():
    total=[]
    for x in range(1,6):
        lotlist=[]
        antibodies=session.query(AntibodyLot).filter(AntibodyLot.antibody_id==x).all()
        for antibody in antibodies:
            lotlist.append(antibody.id)
        total.append(lotlist)
    return total

def cytotoxinlot():
    total=[]
    for x in range(1,6):
        lotlist=[]
        cytotoxins=session.query(CytotoxinLot).filter(CytotoxinLot.cytotoxin_id==x).all()
        for cytotoxin in cytotoxins:
            lotlist.append(cytotoxin.id)
        total.append(lotlist)
    return total

print antibodylot()
print cytotoxinlot()



adcs=session.query(ADCLot).all()
for adc in adcs:
    print adc.id, adc.adc_id, adc.antibodylot_id, adc.cytotoxin_lot_id
