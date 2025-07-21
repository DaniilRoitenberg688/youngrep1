from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (BooleanField, IntegerRangeField, PasswordField,
                     SelectField, StringField, SubmitField, TextAreaField,
                     ValidationError)
from wtforms.validators import DataRequired

from app import models


class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")


class AddTeacherForm(FlaskForm):
    name = StringField("Name")
    surname = StringField("Surname")
    student_class = StringField("Student class")
    tariff = StringField("Tariff")
    school = StringField("School")
    about_text = TextAreaField("About")
    image_link = StringField("Image link")
    image = FileField("Image")

    all_achievements: list
    all_hobbies: list
    all_subjects: list

    achievements_text = TextAreaField("Achievements text")

    hobbies_text = TextAreaField("Hobbies")

    feedback = IntegerRangeField("Feedback")

    free_text = TextAreaField("Free text")

    submit = SubmitField("Add")

    def validate_student_class(self, student_class):
        if student_class.data and not student_class.data.isdigit():
            raise ValidationError("Student class must be a digit")

    def validate_tariff(self, tariff):
        if tariff.data and not tariff.data.isdigit():
            raise ValidationError("Tariff must be a digit")


class EditTeacherForm(AddTeacherForm):
    subjects: list
    achievements: list
    hobbies: list
    image_path: str
    submit = SubmitField("Edit")


class EditSearchForm(FlaskForm):
    subjects: list
    hobbies: list
    achievements: list
    is_free: bool
    submit = SubmitField("Save")


class AddSearchForm(FlaskForm):
    a = {"Предмет": "Предмет", "Достижение": "Достижение", "Хобби": "Хобби"}
    category = SelectField("Category", choices=["Предмет", "Достижение", "Хобби"])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Add")


class EditSearchParamForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Edit")


class EditFreeText(FlaskForm):
    text = TextAreaField("Free text")
    submit = SubmitField("Edit")


class AddCommentForm(FlaskForm):
    user_name = StringField("Name")
    comment = TextAreaField("Comment")
    submit = SubmitField("New comment")
    feedback = IntegerRangeField("Feedback")

    def validate_user_name(self, user_name):
        if not user_name.data:
            raise ValidationError("No user name")

    def validate_comment(self, comment):
        if not comment.data:
            raise ValidationError("No comment text")


class EditCommentForm(AddCommentForm):
    submit = SubmitField("Edit comment")
