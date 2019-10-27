import os
from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from insta_backend.app import create_app
from insta_backend.config import DevConfig, ProdConfig, TestConfig

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

if __name__ == '__main__':
    manager.run()
