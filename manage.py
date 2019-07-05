import subprocess, os

from flask_script import Manager, Server
from apps.core import create_app

manager = Manager(create_app(os.getenv('FLASK_ENV', 'default')))
# run flask server at (0.0.0.0:5000)
manager.add_command('runserver', Server())

## improve to use flask-cli command
@manager.command
def test(test_name=''):
    "Run tests"
    if test_name:
        subprocess.run(['nose2', 'tests.unit_tests.%s' % (test_name), '-v'])
    else:
        subprocess.run(['nose2', '-v'])

if __name__ == '__main__':
    manager.run()
