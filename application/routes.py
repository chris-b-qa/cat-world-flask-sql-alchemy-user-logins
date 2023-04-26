#!/usr/bin/python

from application import app, db
from flask import flash, render_template, redirect, abort, session, request
from application.models import User, Cat
from werkzeug.datastructures import MultiDict
from application.forms import UserForm, CatForm, DeleteForm, EditForm, LoginForm
from sqlalchemy.sql.functions import now

CAT_FORM_DATA = 'cat_form'
USER_FORM_DATA = 'user_form'
LOGGED_IN_USER = 'user_id'
# ---------------------- User routes ----------------------


@app.route('/login')
def login():
    login_form = LoginForm()
    return render_template("/login.html", login_form=login_form)


@app.route('/login', methods=['POST'])
def validate_login():
    login_form = LoginForm()

    if login_form.validate():
        user = db.session.execute(db.select(User).where(User.email == login_form.email.data)).scalars().first()

        if user is not None and user.is_correct_password(login_form.password.data):
            session[LOGGED_IN_USER] = user.id

            user.last_login = now()
            db.session.commit()

            flash(f'{user.name} logged in successfully!')
            return redirect('/')

    flash(f'Could not log in')
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop(LOGGED_IN_USER)
    flash(f'Logged out successfully!')
    return redirect('/')


@app.route('/users')
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return render_template("/users.html", users=users)


@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    edit_form = EditForm()
    delete_form = DeleteForm()
    return render_template('user.html', user=user, edit_form=edit_form, delete_form=delete_form)


@app.route('/users', methods=['POST'])
def create_user():
    user_form = UserForm()

    if user_form.validate():
        new_user = User(name=user_form.name.data, password=user_form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash(f'{new_user.name} added successfully!')
        return redirect('/')

    session[USER_FORM_DATA] = request.form
    return redirect('/')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'{user.name} has been deleted!')
    return redirect('/')


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    edit_form = EditForm()

    if edit_form.validate():
        user = db.get_or_404(User, user_id)
        user.name = edit_form.name.data
        db.session.commit()
        flash(f'{user.name} has been updated!')
        return redirect(f'/users/{ user_id }')

    return abort(400)

# # ---------------------- Cat routes ----------------------


@app.route('/cats')
def get_cats():
    cats = db.session.execute(db.select(Cat)).scalars().all()
    return render_template("/cats.html", cats=cats)


@app.route('/cats/<int:cat_id>')
def get_cat(cat_id):
    cat = db.get_or_404(Cat, cat_id)
    delete_form = DeleteForm()
    edit_form = EditForm()
    return render_template('cat.html', cat=cat, edit_form=edit_form, delete_form=delete_form)


@app.route('/cats', methods=['POST'])
def create_cat():
    cat_form = CatForm()
    cat_form.update_owners()

    if cat_form.validate():
        new_cat = Cat()
        new_cat.name = cat_form.name.data
        new_cat.owner_id = cat_form.owner_id.data
        db.session.add(new_cat)
        db.session.commit()
        flash(f'{new_cat.name} added successfully!')
        return redirect('/')

    session[CAT_FORM_DATA] = request.form
    return redirect('/')


@app.route('/cats/<int:cat_id>/delete', methods=['POST'])
def delete_cat(cat_id):
    cat = db.get_or_404(Cat, cat_id)
    db.session.delete(cat)
    db.session.commit()
    flash(f'{cat.name} has been deleted!')
    return redirect('/')


@app.route('/cats/<int:cat_id>/edit', methods=['POST'])
def edit_cat(cat_id):
    edit_form = EditForm()

    if edit_form.validate():
        cat = db.get_or_404(Cat, cat_id)
        cat.name = edit_form.name.data
        db.session.commit()
        flash(f'{cat.name} has been updated!')
        return redirect(f'/cats/{ cat_id }')

    return abort(400)


@app.route('/')
def index():
    users_count = db.session.query(User).count()
    cats_count = db.session.query(Cat).count()

    cat_form_data = session.get(CAT_FORM_DATA)
    cat_form = CatForm(MultiDict(cat_form_data))
    cat_form.update_owners()

    if cat_form_data is not None:
        session.pop(CAT_FORM_DATA)
        cat_form.validate()

    user_form_data = session.get(USER_FORM_DATA)
    user_form = UserForm(MultiDict(user_form_data))

    if user_form_data is not None:
        session.pop(USER_FORM_DATA)
        user_form.validate()

    logged_in_user_id = session.get(LOGGED_IN_USER)
    logged_in_user = db.session.get(User, logged_in_user_id)

    return render_template('index.html', user_form=user_form, cat_form=cat_form, users_count=users_count,
                           cats_count=cats_count, logged_in_user=logged_in_user)
