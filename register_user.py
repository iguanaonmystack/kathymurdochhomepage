#!/usr/bin/env python3

from getpass import getpass

from kathymurdochhomepage.lib import model_setup
from kathymurdochhomepage.model import User

with open('instance/config.py') as f:
    # includes version
    exec(f.read())

connection = model_setup.setup(SQLOBJECT_DBURI)
connection.debug = True

print('Username:', end=' ')
username = input()
print('Display name:', end=' ')
display_name = input()
password = getpass('Password (will not be shown): ')

user = User.by_username(username)
if not user:
    user = User(username=username, display_name=display_name)
user.display_name = display_name
user.set_password(password)


