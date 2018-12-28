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
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(float)
    radius = Column(float)
    distance = Column(float)

    def __repr__(self):
        return "<User(planet_id='%s', planet_name='%s', planet_type='%s', home_star='%s', mass='%f', radius='%f', " \
               "distance='%f')>" % (self.planet_id, self.planet_name, self.planet_type, self.home_star, self.mass,
                                    self.radius, self.distance)
