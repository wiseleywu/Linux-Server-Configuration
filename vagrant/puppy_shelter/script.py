from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy, Profile, Adopter
import puppypopulator
import datetime

engine=create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()

#Query 1
# puppies=session.query(Puppy).order_by(Puppy.name).all()
# for puppy in puppies:
#     print puppy.name

#Query 2
# today = datetime.date.today()
# puppies=(session.query(Puppy)
#                .filter(Puppy.dateOfBirth>(today-datetime.timedelta(days=180)))
#                .order_by(Puppy.dateOfBirth)
#                .all())
# for puppy in puppies:
#     print puppy.name, puppy.dateOfBirth

#Query3
# puppies=session.query(Puppy).order_by(Puppy.weight).all()
# for puppy in puppies:
#     print puppy.name, puppy.weight

# Query4
# puppies=session.query(Puppy).order_by(Puppy.shelter_id).all()
# for puppy in puppies:
#     print puppy.shelter_id, puppy.name

#Testing one-to-one relationship between profile and puppy
# profiles=session.query(Profile).all()
# for profile in profiles:
#     print profile.id, profile.description, profile.puppy.id
# puppies=session.query(Puppy).all()
# for puppy in puppies:
#     print puppy.id, puppy.name, puppy.profile

#Testing many-to-many relationship between puppy and adopter
# adopted_puppy=session.query(Puppy).filter(Puppy.id==35).first()
# print adopted_puppy.name, adopted_puppy.id, adopted_puppy.adopter
# adopted_puppy.adopter.append(Adopter(name='Jimmy',gender='male'))
# # print adopted_puppy.name, adopted_puppy.id, adopted_puppy.adopter[0].name
# for adopter in adopted_puppy.adopter:
#     print adopter.name, adopter.gender
# person=session.query(Adopter).first()
# print person.name, person.gender, person.puppy
# for puppy in person.puppy:
#     print puppy.name, puppy.id, puppy.adopter[0].name

#Testing checkOut procedure
# adopter1=Adopter(name='Amy', gender='female')
# adopter2=Adopter(name='Bill', gender='male')
# adopter3=Adopter(name='Cathy', gender='female')
# adopter4=Adopter(name='David', gender='male')
# session.add_all([adopter1,adopter2,adopter3,adopter4])
# session.commit()
# adopters=session.query(Adopter).all()
# for adopter in adopters:
#     print adopter.id, adopter.name
# puppypopulator.checkOut(5,[1,2,3,4])
# puppy=session.query(Puppy).filter(Puppy.id==5).first()
# for owner in puppy.adopter:
#     print owner.id, owner.name

# owners=session.query(Adopter).all()
# for owner in owners:
#     for puppy in owner.puppy:
#         print puppy.id, puppy.name
# print session.query(Shelter).filter(Shelter.id==4).first().occupancy
