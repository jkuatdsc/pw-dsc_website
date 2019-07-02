import subprocess

from flask_script import Manager, Server
from core import create_app

manager = Manager(create_app)
# run flask server at (0.0.0.0:5000)
manager.add_command('runserver', Server())

## improve to use flask-cli command
@manager.command
def test():
    "Run tests"
    subprocess.run(['nose2', '-v'])

if __name__ == '__main__':
    manager.run()
