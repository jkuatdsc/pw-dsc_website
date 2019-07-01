from flask_script import Manager, Server
from core import create_app

manager = Manager(create_app)

# run flask server at (0.0.0.0:5000)
manager.add_command('runserver', Server())

if __name__ == '__main__':
    manager.run()
