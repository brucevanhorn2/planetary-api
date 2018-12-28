from flask import Flask, jsonify, request
app = Flask(__name__)


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
    # TODO:  add a data access layer


@app.route('/login/<string:email>/<string:password>', methods=['GET','POST'])
def login(email: str, password: str):
    if email and password:
        return jsonify(message="Login succeeded")
    else:
        return jsonify(message="No empty strings allowed!"), 401


@app.route('/planets', methods=['GET'])
def planets():
    pass


@app.route('/planet_details/<int:planet_id')
def planet_details(planet_id: int):
    pass


@app.route('/add_planet', methods=['POST'])
def add_planet():
    pass


@app.route('/update_planet', methods=['PUT'])
def update_planet():
    pass


@app.route('/remove_planet', methods=['DEL'])
def remove_planet():
    pass


if __name__ == '__main__':
    app.run()
