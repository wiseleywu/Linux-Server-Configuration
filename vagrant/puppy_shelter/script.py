from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy
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
puppies=session.query(Puppy).order_by(Puppy.shelter_id).all()
for puppy in puppies:
    print puppy.shelter_id, puppy.name
