# flake8: noqa

# import dev_appserver
# dev_appserver.fix_sys_path()

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from bot.app import app
from bot.model import *  # noqa

migrate = Migrate(app, db)  # noqa
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
