import os
from app import create_app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server
from flask import abort, request
import logging
import pytz

logging.basicConfig(filename='admin.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(threadName)-10s: %(message)s',)

config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
manager = Manager(app)
migrate = Migrate(app, db)
tz = pytz.timezone('Asia/Jakarta')

@manager.command
def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def create_db():
    from sqlalchemy_utils import create_database, database_exists
    if not database_exists(os.getenv('DATABASE_URI')):
        create_database(os.getenv('DATABASE_URI'))


manager.add_command('runserver', Server(host='0.0.0.0', port=5000, threaded=True))

if __name__ == '__main__':
    manager.run()