#!/usr/bin/python

from application import db, app
from application.models import User, Cat

USERS = [
    User(name='Steve', email='steve@example.com', password='password'),
    User(name='Bob', email='bob@example.com', password='password1'),
    User(name='Mike', email='mike@example.com', password='p@ssw0rd'),
]

cats = [
    {'name': 'Tibbles', 'owner_name': 'Steve'},
    {'name': 'Ginger', 'owner_name': None},
    {'name': 'Meow', 'owner_name': 'Steve'},
    {'name': 'Tabby', 'owner_name': 'Mike'},
]

with app.app_context():
    db.session.add_all(USERS)
    db.session.commit()

    user_models = dict(db.session.execute(db.select(User.name, User.id)).all())

    for cat in cats:
        if cat['owner_name'] is not None and cat['owner_name'] in user_models.keys():
            cat['owner_id'] = user_models[cat['owner_name']]

    db.session.bulk_insert_mappings(Cat, cats)
    db.session.commit()

print('Database seeded successfully!')
