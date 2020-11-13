# Do DB-Stuff
# python3 -m pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

engine = create_engine('sqlite:///test.db', echo=False)
Base = declarative_base()


class Child(Base):
    ''' The Child '''
    __tablename__ = 'childs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    father_id = Column(Integer, ForeignKey('fathers.id'))
    father = relationship("Father", back_populates="childs")
    
    def __init__(self, name, father):
        self.name = name
        self.father = father

class Father(Base):
    ''' The Father '''
    __tablename__ = 'fathers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    childs = relationship("Child", order_by=Child.id, back_populates="father")


    def __init__(self, name="Hans", last_name="Bauer"):
        self.name = name
        self.last_name = last_name
        self.hello_world()

    def hello_world(self):
        print("Hello World {}".format(self.name))


# Create tables
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Create objects
# father = Father()
# child = Child("Kind", father)

# Create objects
# session.add(father)
# session.commit()
# session.add(child)
# session.commit()

# Show all fathers with all children
# for entry in session.query(Father).all():
#     print(entry.name)
#     for child in entry.childs:
#         print(child.name)

