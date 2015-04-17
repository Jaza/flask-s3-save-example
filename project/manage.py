#!/usr/bin/env python

from __future__ import print_function

# Set the path
from os import path
import sys
sys.path.append(path.abspath(path.join(path.dirname(__file__), '..')))

from flask_script import Manager, Server
from flask_script.commands import InvalidCommand
from flask_migrate import MigrateCommand


def create_app(quiet=False):
    from project import app

    return app


manager = Manager(create_app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

manager.add_command('db', MigrateCommand)


from accounts.commands import *


if __name__ == "__main__":
    manager.run()
