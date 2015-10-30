from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Antibody(Base):
    __tablename__='antibody'
    name=Column(String(80), nullable=False)
    id=Column(Integer, primary_key=True)
    weight=Column(Float, nullable=False)
    target=Column(String(80), nullable=False)
    picture=image_attachment('AntibodyImg')

class AntibodyImg(Base, Image):
    __tablename__='antibody_img'
    antibody_id=Column(Integer, ForeignKey('antibody.id'), primary_key=True)
    antibody=relationship('Antibody')

class AntibodyLot(Base):
    __tablename__='antibody_lot'
    id=Column(Integer, primary_key=True)
    date=Column(Date, nullable=False)
    aggregate=Column(Float, nullable=False)
    endotoxin=Column(Float, nullable=False)
    concentration=Column(Float, nullable=False)
    vialVolume=Column(Float, nullable=False)
    vialNumber=Column(Integer, nullable=False)
    antibody_id=Column(Integer, ForeignKey('antibody.id'))
    antibody=relationship('Antibody')

class Cytotoxin(Base):
    __tablename__='cytotoxin'
    name=Column(String(80), nullable=False)
    id=Column(Integer, primary_key=True)
    weight=Column(Float, nullable=False)
    drugClass=Column(String(80), nullable=False)
    picture=image_attachment('CytotoxinImg')

class CytotoxinImg(Base, Image):
    __tablename__='cytotoxin_img'
    cytotoxin_id=Column(Integer, ForeignKey('cytotoxin.id'), primary_key=True)
    cytotoxin=relationship('Cytotoxin')

class CytotoxinLot(Base):
    __tablename__='cytotoxin_lot'
    id=Column(Integer, primary_key=True)
    date=Column(Date, nullable=False)
    purity=Column(Float, nullable=False)
    concentration=Column(Float, nullable=False)
    vialVolume=Column(Float, nullable=False)
    vialNumber=Column(Integer, nullable=False)
    cytotoxin_id=Column(Integer, ForeignKey('cytotoxin.id'))
    cytotoxin=relationship('Cytotoxin')

class ADC(Base):
    __tablename__='adc'
    name=Column(String(80), nullable=False)
    chemistry=Column(String(80), nullable=False)
    id=Column(Integer, primary_key=True)

class ADCLot(Base):
    __tablename__='adc_lot'
    id=Column(Integer, primary_key=True)
    date=Column(Date, nullable=False)
    aggregate=Column(Float, nullable=False)
    endotoxin=Column(Float, nullable=False)
    concentration=Column(Float, nullable=False)
    vialVolume=Column(Float, nullable=False)
    vialNumber=Column(Integer, nullable=False)
    adc_id=Column(Integer, ForeignKey('adc.id'))
    adc=relationship('ADC')
    antibodylot_id=Column(Integer, ForeignKey('antibody_lot.id'))
    antibodylot=relationship(AntibodyLot)
    cytotoxin_lot_id=Column(Integer, ForeignKey('cytotoxin_lot.id'))
    cytotoxin_lot=relationship(CytotoxinLot)

    @property
    def serialize(self):
        return {
            'id':self.id,
            'date':self.date,
            'aggregate':self.aggregate,
            'endotoxin':self.endotoxin,
            'concentration':self.concentration,
            'vialVolume':self.vialVolume,
            'vialNumber':self.vialNumber,
        }

############################insert at end of file #############################
engine = create_engine('sqlite:///biologicscatalog.db')
Base.metadata.create_all(engine)
