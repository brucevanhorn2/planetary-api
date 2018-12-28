from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Column, Integer, String, Float
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

db = SQLAlchemy(app)
mail = Mail(app)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    def __repr__(self):
        return "<User(first_name='%s', last_name='%s', email='%s', password='%s')>" % (
            self.first_name, self.last_name, self.email, self.password)


class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String, unique=True)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

    def __repr__(self):
        return "<Planet(planet_id='%s', planet_name='%s', planet_type='%s', home_star='%s', mass='%f', radius='%f', " \
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
    email = request.form['email']

    test = User.query.filter_by(email=email).first()

    if test:
        return jsonify(message="That email already exists"), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully"), 201


@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    user = User.query.filter_by(email=email)
    if user:
        msg = Message("Your planetary API password is: " + user.password,
                      sender="admin@planetary-api.com",
                      recipients=[email])
        mail.send(msg)
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message="That email doesn't exist."), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    test = User.query.filter_by(email=email, password=password)
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


@app.route('/planets', methods=['GET'])
def planets():
    return jsonify(Planet.query.all())


@app.route('/planet_details/<int:planet_id>')
def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        return jsonify(planet)
    else:
        return jsonify(message="That planet does not exist"), 404


@app.route('/add_planet', methods=['POST'])
@jwt_required
def add_planet():
    planet_name = request.form['planet_name']
    test = Planet.query.filter_by(planet_name=planet_name)
    if test:
        return jsonify(message="There is already a planet with that name"), 409
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        circumference = float(request.form['radius'])
        radius = float(request.form['distance'])

        new_planet = Planet(planet_name=planet_name,
                            planet_type=planet_type,
                            home_star=home_star,
                            mass=mass,
                            circumference=circumference,
                            radius=radius)

        db.session.add(new_planet)
        db.session.commit()

        return jsonify(message="You added a planet"), 201


@app.route('/update_planet', methods=['PUT'])
@jwt_required
def update_planet():
    planet_id = int(request.form['planet_id'])

    planet = Planet.query.filter_by(planet_id=planet_id)
    if planet:
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.radius = float(request.form['radius'])
        planet.distance = float(request.form['distance'])
        db.session.commit()
        return jsonify(message="You updated a planet")
    else:
        return jsonify(message="That planet does not exist"), 404


@app.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
@jwt_required
def remove_planet(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        return jsonify(message="You deleted a planet: " + str(planet_id))
    else:
        return jsonify(message="That planet doesn't exist."), 404


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run()
