#!/usr/bin/python
from application import db, app

with app.app_context():
    db.create_all()

print('Migrations ran successfully!')
