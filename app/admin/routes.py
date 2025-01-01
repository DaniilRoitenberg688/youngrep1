from urllib.parse import urlsplit
import os

from app import app, db, subjects, hobbies, achievements
from app.admin import bp
from flask import render_template, redirect, url_for, flash, request
from app.admin.forms import LoginForm, AddTeacherForm
from flask_login import current_user, login_user, login_required, logout_user

from app.models import User, Teacher, Subject, Achievement, Hobby


@bp.route('/')
@login_required
def index():
    teachers = []
    data = request.args
    if not data:
        teachers = Teacher.query.all()

    if data.getlist('hobbies'):
        for hobby in data.getlist('hobbies'):
            hobby: Hobby = Hobby.query.filter_by(name=hobby).first()
            teachers.extend(hobby.teachers)

    if data.getlist('achievements'):
        for achievement in data.getlist('achievements'):
            achievement: Achievement = Achievement.query.filter_by(name=achievement).first()
            teachers.extend(achievement.teachers)

    if data.getlist('subjects'):
        for subject in data.getlist('subjects'):
            subject: Achievement = Achievement.query.filter_by(name=subject).first()
            teachers.extend(subject.teachers)

    if data.get('age'):
        teachers.append(Teacher.query.filter_by(students_age=int(data.get('age'))
                                                ).first())

    if data.get('tariff'):
        teachers.extend(Teacher.query.filter(Teacher.tariff<=int(data.get('tariff'))).all())



    teachers = list(set(teachers))

    return render_template('admin/index.html', title='Teachers', teachers=teachers, all_subjects=subjects,
                           all_achievements=achievements, all_hobbies=hobbies)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(login=form.login.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Wrong password or username')
            return redirect(url_for('admin.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('admin.index')
        return redirect(next_page)
    return render_template('admin/login.html', form=form, title='Login')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.index'))


@bp.route('/teacher', methods=['GET', 'POST'])
@login_required
def new_teacher():
    form = AddTeacherForm()
    if form.validate_on_submit():

        teacher = Teacher(
            name=form.name.data,
            surname=form.surname.data,
            students_class=form.student_class.data,
            school=form.school.data,
            about_text=form.about_text.data,
            tariff=form.tariff.data,
            feedback=form.feedback.data,
            achievements_text=form.achievements_text.data,
            hobbies_text=form.hobbies_text.data
        )

        db.session.add(teacher)

        subjects = request.form.getlist('subjects')
        achievements = request.form.getlist('achievements')
        hobbies = request.form.getlist('hobbies')
        for subject in subjects:
            subject: Subject = Subject.query.filter_by(name=subject).first()
            teacher.subjects.append(subject)

        for achievement in achievements:
            achievement: Achievement = Achievement.query.filter_by(name=achievement).first()
            print(achievement.teachers)
            teacher.achievements.append(achievement)

        for hobby in hobbies:
            hobby: Hobby = Hobby.query.filter_by(name=hobby).first()
            teacher.hobbies.append(hobby)

        db.session.commit()

        image = form.image.data
        if image is not None:
            image.save(os.path.join(app.config['UPLOAD_PATH'], str(teacher.id) + '.png'))
            teacher.image = str(teacher.id) + '.png'
            db.session.commit()

        return redirect(url_for('admin.index'))

    return render_template('admin/add_teacher.html', form=form)


@bp.route('/teacher/<int:id>', methods=['GET', 'DELETE'])
@login_required
def delete_teacher(id):
    teacher = db.session.get(Teacher, id)
    if teacher.image:
        os.remove(os.path.join(app.config['UPLOAD_PATH'], teacher.image))
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for('admin.index'))


@bp.route('/search_form', methods=['POST'])
@login_required
def search_form():
    subjects = request.form.getlist('subjects')
    age = request.form.getlist('age')
    achievements = request.form.getlist('achievements')
    tariff = request.form.get('tariff')
    hobbies = request.form.get('hobbies')
    return redirect(url_for('admin.index', subjects=subjects, age=age, achievements=achievements, tariff=tariff,
                            hobbies=hobbies))
