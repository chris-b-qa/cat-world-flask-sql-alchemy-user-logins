#!/usr/bin/python

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

from application.database import db
from application.models import User


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Add User')


class CatForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    owner_id = SelectField('Owner', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Add Cat')

    def update_owners(self):
        self.owner_id.choices = [(user.id, user.name) for user in db.session.execute(db.select(User)).scalars()]


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')


class EditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Save changes')
