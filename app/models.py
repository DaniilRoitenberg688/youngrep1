from enum import unique

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

@login.user_loader
def load_user(id):
    return db.session.get(User, id)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    surname = db.Column(db.String(), nullable=True)
    students_class = db.Column(db.Integer, nullable=True)
    school = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Integer, nullable=True)
    about_text = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(), nullable=True)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'))
    subject = db.relationship('Subject', backref=db.backref('teachers'))

    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id', ondelete='CASCADE'))
    achievement = db.relationship('Achievement', backref=db.backref('teachers'))

    hobby_id = db.Column(db.Integer, db.ForeignKey('hobby.id', ondelete='CASCADE'))
    hobby = db.relationship('Hobby', backref=db.backref('teachers'))


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

    def __repr__(self):
        return f'Subject <{self.name}>'

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

    def __repr__(self):
        return f'Achievement <{self.name}>'


class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

    def __repr__(self):
        return f'Hobby <{self.name}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


