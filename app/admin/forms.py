
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, widgets, IntegerRangeField, ValidationError
from wtforms.fields.choices import SelectMultipleField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField

from app import models
from flask import current_app



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
    tariff = StringField('Tariff')
    school = StringField('School')
    about_text = TextAreaField('About')
    image_link = StringField('Image link')
    image = FileField('Image')

    achievements_text = TextAreaField('Achievements text')

    hobbies_text = TextAreaField('Hobbies')

    feedback = IntegerRangeField('Feedback')

    submit = SubmitField('Add')


    def validate_student_class(self, student_class):
        if student_class.data and not student_class.data.isdigit():
            raise ValidationError('Student class must be a digit')


    def validate_tariff(self, tariff):
        if tariff.data and not tariff.data.isdigit():
            raise ValidationError('Tariff must be a digit')




class EditTeacherForm(AddTeacherForm):
    subjects: list
    achievements: list
    hobbies: list
    image_path: str
    submit = SubmitField('Edit')







