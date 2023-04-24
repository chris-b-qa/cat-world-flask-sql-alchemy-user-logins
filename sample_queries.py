#!/usr/bin/python
"""A selection of sample queries on the seeded dataset"""

from application import app, db, User, Cat

# We have to use app.app_context() as the application isn't actually running in this file
with app.app_context():
    # Select all users
    all_users = db.session.execute(db.select(User)).scalars().all()
    print(f'All user objects: {all_users}')
    print(f'All user\'s names: {[user.name for user in all_users]}')

    # Select user with a particular id
    user_two = db.session.get(User, 2)
    print(f'User two object: {user_two}')
    print(f'User two name: {user_two.name}')

    # Select a user with a particular name
    mike = db.session.execute(db.select(User).filter_by(name='Mike')).scalar()
    print(f'mike object: {mike}')
    print(f'mike id: {mike.id}')

    # Select a user with a particular name - alternative method
    mike = db.session.execute(db.select(User).where(User.name == 'Mike')).scalar()
    print(f'mike object: {mike}')
    print(f'mike id: {mike.id}')

    # Show that user's cats
    print(f'Mike\'s cats as objects: {mike.cats}')
    print(f'Mike\'s cats\' names: {[cat.name for cat in mike.cats]}')

    # Select just a specific column
    user_one_name = db.session.execute(db.select(User.name).where(User.id == 1)).scalar()
    print(f'User one name: {user_one_name}')

    # Select all users in alphabetical order
    all_users_alphabetical = db.session.execute(db.select(User).order_by(User.name)).scalars().all()
    print(f'All users in alphabetical order: {all_users_alphabetical}')
    print(f'All users names in alphabetical order: {[user.name for user in all_users_alphabetical]}')

    # Select all users by reverse alphabetical order
    all_users_reverse_alphabetical = db.session.execute(db.select(User).order_by(User.name.desc())).scalars().all()
    print(f'All users in reverse alphabetical order: {all_users_reverse_alphabetical}')
    print(f'All users names in reverse alphabetical order: {[user.name for user in all_users_reverse_alphabetical]}')

    # Select all users that have an e at the end
    users_with_an_e = db.session.execute(db.select(User).where(User.name.like('%e'))).scalars().all()
    print(f'The following users name end with an e: {[user.name for user in users_with_an_e]}')

    # Insert a new user
    new_user = User()
    new_user.name = "A new user"
    db.session.add(new_user)
    db.session.commit()

    # Get the number of users with the name "A new user"
    new_user_count = db.session.query(User).where(User.name == 'A new user').count()
    print(f'We have {new_user_count} users with the name "A new user"')

    # Insert a User and their Cats with models
    cat_owner = User()
    cat_owner.name = "Cat Owner"

    new_cat = Cat()
    new_cat.name = "New Cat"
    cat_owner.cats.append(new_cat)

    # Ensure we persist both the new user and the new cat!
    db.session.add(new_user)
    db.session.add(new_cat)
    db.session.commit()
    print(f'Cat Owner\'s cat is called: {cat_owner.cats[0].name}')

    # Lets rename that cat
    new_cat.name = 'Georgina'
    db.session.commit()
    print(f'Cat Owner\'s cat is now called: {cat_owner.cats[0].name}')

    # Let's delete those new rows and keep things tidy
    db.session.delete(new_cat)
    db.session.delete(cat_owner)
    db.session.delete(new_user)
    db.session.commit()
    print(f'All those items have now been deleted!')
