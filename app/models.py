from email.policy import default
from enum import unique

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login


@login.user_loader
def load_user(id):
    return db.session.get(User, id)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    enabled = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Subject <{self.name}>'

    def change_value(self):
        self.enabled = not self.enabled


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    enabled = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Achievement <{self.name}>'

    def change_value(self):
        self.enabled = not self.enabled


class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    enabled = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Hobby <{self.name}>'

    def change_value(self):
        self.enabled = not self.enabled


teacher_subject = db.Table('teacher_subject',
                           db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE')),
                           db.Column('subject_id', db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE')))

teacher_achievement = db.Table('teacher_achievement',
                               db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE')),
                               db.Column('achievement_id', db.Integer,
                                         db.ForeignKey('achievement.id', ondelete='CASCADE')))

teacher_hobby = db.Table('teacher_hobby',
                         db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE')),
                         db.Column('hobby_id', db.Integer, db.ForeignKey('hobby.id', ondelete='CASCADE')))


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    surname = db.Column(db.String(), nullable=True)
    students_class = db.Column(db.Integer, nullable=True, index=True)
    tariff = db.Column(db.Integer, nullable=True, index=True)
    school = db.Column(db.String(), nullable=True)
    feedback = db.Column(db.Integer, nullable=True)
    about_text = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(), nullable=True)

    achievements_text = db.Column(db.Text, nullable=True)
    hobbies_text = db.Column(db.Text, nullable=True)

    subjects = db.relationship('Subject', secondary=teacher_subject, backref=db.backref('teachers'))

    achievements = db.relationship('Achievement', secondary=teacher_achievement, backref=db.backref('teachers'))

    hobbies = db.relationship('Hobby', secondary=teacher_hobby, backref=db.backref('teachers'))

    is_free = db.Column(db.Boolean, nullable=True, default=False)

    # free_text = db.Column(db.Text, nullable=True)

    schedule = db.Column(db.String())
    is_shown = db.Column(db.Boolean, nullable=True, default=True)

    shown_times = db.Column(db.Integer, default=0)

    position = db.Column(db.Integer)

    def __init__(self, name, surname, students_class, tariff, school, about_text, achievements_text,
                 hobbies_text, is_free):
        self.name = name
        self.surname = surname
        self.students_class = students_class
        self.tariff = tariff
        self.school = school
        self.about_text = about_text
        self.achievements_text = achievements_text
        self.hobbies_text = hobbies_text
        self.is_free = is_free
        # self.free_text = free_text


    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'position': self.position
        }

    def parse_schedule(self):
        result = {}
        if self.schedule:
            days = self.schedule.split(';')
            for day in days:
                day = day.split()
                result[day[0]] = day[1:]
        else:
            pass


        return result

    def set_schedule(self, schedule: dict):
        result = []
        print(result)
        if not schedule:
            for day in ['Mon', 'Tue', 'Wen', 'Thu', 'Fri', 'Sat', 'Sun']:
                print(day)
                result.append(' '.join([day]))
        else:
            for day, times in schedule.items():
                a = [day]
                a.extend(times)
                print(a)
                result.append(' '.join(a))

        print(result)
        self.schedule = ';'.join(result)




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    password_hash = db.Column(db.String)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'))
    teacher = db.relationship('Teacher')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    quantity = db.Column(db.Integer, default=0)
    description = db.Column(db.String())


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String())
    text = db.Column(db.Text)
    feedback = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'))
    teacher = db.relationship('Teacher', backref=db.backref('comments'))
