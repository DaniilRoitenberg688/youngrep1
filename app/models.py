from sqlalchemy.orm import backref

from app import db


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


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

    def __repr__(self):
        return f'Subject <{self.name}>'

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)