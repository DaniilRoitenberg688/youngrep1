from enum import unique

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

@login.user_loader
def load_user(id):
    return db.session.get(User, id)

teacher_subject = db.Table('teacher_subject',
                           db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), primary_key=True),
                           db.Column('subject_id', db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), primary_key=True))

teacher_achievement = db.Table('teacher_achievement',
                           db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), primary_key=True),
                           db.Column('achievement_id', db.Integer, db.ForeignKey('achievement.id', ondelete='CASCADE'), primary_key=True))

teacher_hobby = db.Table('teacher_hobby',
                           db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), primary_key=True),
                           db.Column('hobby_id', db.Integer, db.ForeignKey('hobby.id', ondelete='CASCADE'), primary_key=True))


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    surname = db.Column(db.String(), nullable=True)
    students_class = db.Column(db.Integer, nullable=True, index=True)
    school = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Integer, nullable=True)
    about_text = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(), nullable=True)

    achievements_text = db.Column(db.Text, nullable=True)
    hobbies_text = db.Column(db.Text, nullable=True)


    subjects = db.relationship('Subject', secondary=teacher_subject, backref=db.backref('teachers'))

    achievements = db.relationship('Achievement', secondary=teacher_achievement, backref=db.backref('teachers'))

    hobbies = db.relationship('Hobby', secondary=teacher_hobby, backref=db.backref('teachers'))


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


