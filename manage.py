from app import app, db
from flask_script import Manager, prompt_bool


manager = Manager(app)

@manager.command
def init_db():
    db.create_all()
    print('Created database')


@manager.command
def drop_db():
    if prompt_bool("Are you sure?"):
        db.drop_all()
        print ('Database dropped')


if __name__ == '__main__':
    manager.run()
