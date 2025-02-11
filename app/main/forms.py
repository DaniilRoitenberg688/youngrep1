from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, \
    IntegerRangeField, ValidationError


class AddCommentForm(FlaskForm):
    user_name = StringField('Ваше имя')
    comment = TextAreaField('Ваш отзыв')
    submit = SubmitField('Оставить отзыв')
    feedback = IntegerRangeField('Оценка')

    def validate_user_name(self, user_name):
        if not user_name.data:
            raise ValidationError('Введите имя')

    def validate_comment(self, comment):
        if not comment.data:
            raise ValidationError('Введите отзыв')


class EditCommentForm(AddCommentForm):
    submit = SubmitField('Edit comment')
