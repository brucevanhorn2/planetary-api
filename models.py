from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(first_name='%s', last_name='%s', email='%s', password='%s')>" % (
            self.first_name, self.last_name, self.email, self.password)


class Planet(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    mass = Column(float)
    distance = Column(float)

    def __repr__(self):
        return "<Planet(planet_name='%s', mass='%f', distance='%f')>" % (
            self.planet_name, self.mass, self.distance)
