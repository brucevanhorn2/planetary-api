from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
db = SQLAlchemy(app)


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
    return jsonify(first_name=first_name, last_name=last_name, email=email, password=password)
    # TODO:  add a data access layer


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    return jsonify(message="Login succeeded")


@app.route('/planets', methods=['GET'])
def planets():
    return jsonify(message="This is a list of planets")


@app.route('/planet_details/<int:planet_id>')
def planet_details(planet_id: int):
    return jsonify(message="You asked about planet " + str(planet_id))


@app.route('/add_planet', methods=['POST'])
def add_planet():
    planet_name = request.form['planet_name']
    planet_type = request.form['planet_type']
    home_star = request.form['home_star']
    mass = float(request.form['mass'])
    circumference = float(request.form['radius'])
    radius = float(request.form['distance'])

    return jsonify(message="You added a planet")


@app.route('/update_planet', methods=['PUT'])
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet_name = request.form['planet_name']
    planet_type = request.form['planet_type']
    home_star = request.form['home_star']
    mass = float(request.form['mass'])
    radius = float(request.form['radius'])
    distance = float(request.form['distance'])
    return jsonify(message="You updated a planet")


@app.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
def remove_planet(planet_id: int):
    return jsonify(message="You deleted a planet: " + str(planet_id))


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run()
