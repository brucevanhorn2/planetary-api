from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(first_name='%s', last_name='%s', email='%s', password='%s')>" % (
            self.first_name, self.last_name, self.email, self.password)


class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

    def __repr__(self):
        return "<User(planet_id='%s', planet_name='%s', planet_type='%s', home_star='%s', mass='%f', radius='%f', " \
               "distance='%f')>" % (self.planet_id, self.planet_name, self.planet_type, self.home_star, self.mass,
                                    self.radius, self.distance)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple', methods=['GET'])
def super_simple():
    return jsonify(message='Hello from the Planetary API')


@app.route('/parameters/<string:name>/<int:age>', methods=['GET'])
def parameters(name: str, age: int):
    if age < 18:
        return jsonify(message=str(age) + " is too low."), 401
    else:
        return jsonify(name=name.upper(), ageNextYear=age + 1), 200


@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify(first_name=first_name, last_name=last_name, email=email)


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    return jsonify(message="Login succeeded")


@app.route('/planets', methods=['GET'])
def planets():
    return jsonify(Planet.query.all())


@app.route('/planet_details/<int:planet_id>')
def planet_details(planet_id: int):
    return jsonify(Planet.query.filter_by(planet_id=planet_id).first())


@app.route('/add_planet', methods=['POST'])
def add_planet():
    planet_name = request.form['planet_name']
    planet_type = request.form['planet_type']
    home_star = request.form['home_star']
    mass = float(request.form['mass'])
    circumference = float(request.form['radius'])
    radius = float(request.form['distance'])

    new_planet = Planet(planet_name=planet_name, planet_type=planet_type, home_star=home_star,
                        mass=mass, circumference=circumference, radius=radius)

    db.session.add(new_planet)
    db.session.commit()

    return jsonify(message="You added a planet")


@app.route('/update_planet', methods=['PUT'])
def update_planet():
    planet_id = int(request.form['planet_id'])

    planet = Planet.query.filter_by(planet_id=planet_id)

    planet.planet_name = request.form['planet_name']
    planet.planet_type = request.form['planet_type']
    planet.home_star = request.form['home_star']
    planet.mass = float(request.form['mass'])
    planet.radius = float(request.form['radius'])
    planet.distance = float(request.form['distance'])
    db.session.commit()
    return jsonify(message="You updated a planet")


@app.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
def remove_planet(planet_id: int):
    return jsonify(message="You deleted a planet: " + str(planet_id))


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run()
