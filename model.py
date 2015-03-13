from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, MetaData, Index, BigInteger, Integer, String, ForeignKey, DateTime, Boolean, Text, Float
from sqlalchemy.orm import backref, mapper, relation, sessionmaker

Base = declarative_base()

class Numbers(Base):
    __tablename__ = 'snumbers'

    drawNo = Column(Integer, primary_key=True)
    drawTime = Column(String(19))
    Num1 = Column(Integer)
    Num2 = Column(Integer)
    Num3 = Column(Integer)
    Num4 = Column(Integer)
    Num5 = Column(Integer)
    Num6 = Column(Integer)
    Num7 = Column(Integer)
    Num8 = Column(Integer)
    Num9 = Column(Integer)
    Num10 = Column(Integer)
    Num11 = Column(Integer)
    Num12 = Column(Integer)
    Num13 = Column(Integer)
    Num14 = Column(Integer)
    Num15 = Column(Integer)
    Num16 = Column(Integer)
    Num17 = Column(Integer)
    Num18 = Column(Integer)
    Num19 = Column(Integer)
    Num20 = Column(Integer)

class MStats(Base):
    __tablename__= 'Month_Stats'
    Number = Column(Integer, primary_key=True)
    Times = Column(Integer)
    lastDrawNo = Column(Integer)

class YStats(Base):
    __tablename__= 'Year_Stats'
    Number = Column(Integer, primary_key=True)
    Times = Column(Integer)
    lastDrawNo = Column(Integer)

Index('myindex', Numbers.drawNo)

# create a connection to a sqlite database
# turn echo on to see the auto-generated SQL
engine = create_engine('mysql://tkampour:github@localhost:3306/Kino')
 
# create the table and tell it to create it in the 
# database engine that is passed
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
#Session.add(User(...))
#Session.add_all([User(..),User])
#Session.commit()

