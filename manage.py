import os

from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from insta_backend.app import create_app
from insta_backend.config import DevConfig, ProdConfig, TestConfig

TESTS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests')
env = os.environ.get("INSTA_ENV").lower()
if env == 'prod':
    app = create_app(ProdConfig)
elif env == 'dev':
    app = create_app(DevConfig)
else:
    app = create_app(TestConfig)


manager = Manager(app=app)
manager.add_command('runserver', Server(threaded=True))
manager.add_command('db', MigrateCommand)


@manager.command
@manager.option('-p', '--path', dest='path', default=TESTS_PATH)
def tests(path=TESTS_PATH):
    """Run the tests."""
    exit_code = os.system('export INSTA_ENV=Test;' +
                          'py.test ' + path + ' -W ignore::DeprecationWarning')
    return exit_code


if __name__ == '__main__':
    manager.run()
