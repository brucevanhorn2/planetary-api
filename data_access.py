from sqlalchemy import create_engine
import models
engine = create_engine('sqlite:///:memory:', echo=True)



def get_db():
    pass


def authenticate(email: str, password: str):
    pass


def register(first_name: str, last_name: str, email: str, password: str):
    pass


def read_all_planets():
    pass


def read_planet_detail(planet_id: int):
    pass


def create_planet(planet_name: str, mass: float, circumference: float, distance: float):
    pass


def update_planet(planet_name: str, mass: float, circumference: float, distance: float):
    pass


def delete_planet(planet_name: str, mass: float, circumference: float, distance: float):
    pass

