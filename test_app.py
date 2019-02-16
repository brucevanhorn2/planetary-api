import requests


access_token = ""
base_url = 'http://localhost:5000'


def test_super_simple():
    resp = requests.get('http://localhost:5000/super_simple')
    assert(resp.status_code == 200)
    returned_data = resp.json()
    assert(returned_data['message'] == 'Hello from the Planetary API')


def test_user_create():
    new_user = {'first_name': 'Nicolaus',
                'last_name': 'Copernicus',
                'email': 'nico@hotmail.com',
                'password': 'P@ssw0rd'}

    resp = requests.post("http://localhost:5000/register", data=new_user)
    assert(resp.status_code == 201)
    returned_data = resp.json()
    assert(returned_data['message'] == 'User created successfully')


def test_login():
    login_credentials = {'login': 'nico@hotmail.com', 'password': 'P@ssw0rd'}
    resp = requests.post("http://localhost:5000/login", data=login_credentials)
    assert(resp.status_code == 200)
    returned_data = resp.json()
    access_token = returned_data['token']  # you'll need this in subsequent tests
    assert(access_token is not None)  # make sure it isn't null


def test_planet_create():
    assert False


def test_planet_update():
    assert False


def test_planet_delete():
    assert False
