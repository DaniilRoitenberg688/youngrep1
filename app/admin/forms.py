
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, widgets
from wtforms.fields.choices import SelectMultipleField
from wtforms.validators import DataRequired
from app import app, db
from app.models import Subject
from flask_wtf.file import FileField



class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()


class AddTeacherForm(FlaskForm):
    name = StringField('Name')
    surname = StringField('Surname')
    student_class = StringField('Student class')
    school = StringField('School')
    about_text = TextAreaField('About')
    image_link = StringField('Image link')
    image = FileField('Image')

    with app.app_context():
        all_subjects = Subject.query.all()
        all_subjects = [i for i in all_subjects]

        all_achievements = []

    submit = SubmitField('Add')






