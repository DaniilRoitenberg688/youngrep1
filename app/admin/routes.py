from urllib.parse import urlsplit
import os

from app import app, db, subjects, hobbies, achievements
from app.admin import bp
from flask import render_template, redirect, url_for, flash, request
from app.admin.forms import LoginForm, AddTeacherForm, EditTeacherForm
from flask_login import current_user, login_user, login_required, logout_user

from app.models import User, Teacher, Subject, Achievement, Hobby
import sqlalchemy


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
            subject: Subject = Subject.query.filter_by(name=subject).first()
            teachers.extend(subject.teachers)

    if data.get('age'):
        teachers.extend(Teacher.query.filter_by(students_class=int(data.get('age'))
                                                ).all())

    if data.get('tariff'):
        teachers.extend(Teacher.query.filter(Teacher.tariff <= int(data.get('tariff'))).all())

    if data.get('names'):
        names = data.get('names').split()
        result = []
        if len(names) == 1:
            result = Teacher.query.filter(
                names[0] == Teacher.surname
            ).all()

            if not result:
                result = Teacher.query.filter(
                    names[0] == Teacher.name
                ).all()
        if len(names) == 2:
            result = Teacher.query.filter(
                names[0] == Teacher.surname or names[1] == Teacher.name
            ).all()
            if not result:
                result = Teacher.query.filter(
                    names[1] == Teacher.surname or names[0] == Teacher.name
                ).all()

        teachers.extend(result)

    teachers = list(set(teachers))
    teachers = sorted(teachers, key=lambda x: x.feedback)

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
    return redirect(url_for('main.index'))


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
        db.session.commit()

        hobbies_to_add = request.form.getlist('hobbies')
        for i in hobbies_to_add:
            hobby = Hobby.query.filter(Hobby.name == i).first()
            hobby.teachers
            teacher.hobbies.append(hobby)

        subjects_to_add = request.form.getlist('subjects')
        for i in subjects_to_add:
            subject = Subject.query.filter(Subject.name == i).first()
            subject.teachers
            teacher.subjects.append(subject)

        achievements_to_add = request.form.getlist('achievements')
        for i in achievements_to_add:
            achievement = Achievement.query.filter(Achievement.name == i).first()
            achievement.teachers
            teacher.achievements.append(achievement)

        db.session.commit()

        image = form.image.data
        if image is not None:
            image.save(os.path.join(app.config['UPLOAD_PATH'], str(teacher.id) + '.png'))
            teacher.image = str(teacher.id) + '.png'
            db.session.commit()


        return redirect(url_for('admin.index'))

    return render_template('admin/add_teacher.html', form=form)


@bp.route('/delete_teacher/<int:id>', methods=['GET', 'DELETE'])
@login_required
def delete_teacher(id):
    teacher = db.session.get(Teacher, id)
    if teacher.image:
        os.remove(os.path.join(app.config['UPLOAD_PATH'], teacher.image))
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for('admin.index'))


@bp.route('/edit_teacher/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
    form = EditTeacherForm()
    teacher = db.session.get(Teacher, id)
    if form.validate_on_submit():
        teacher.name = form.name.data
        teacher.surname = form.surname.data
        teacher.tariff = form.tariff.data
        teacher.students_class = form.student_class.data
        teacher.school = form.school.data
        teacher.about_text = form.about_text.data
        teacher.feedback = form.feedback.data
        teacher.achievements_text = form.achievements_text.data
        teacher.hobbies_text = form.hobbies_text.data

        teacher.subjects.clear()
        teacher.hobbies.clear()
        teacher.achievements.clear()

        subjects = request.form.getlist('subjects')
        achievements = request.form.getlist('achievements')
        hobbies = request.form.getlist('hobbies')
        for subject in subjects:
            subject: Subject = Subject.query.filter_by(name=subject).first()
            teacher.subjects.append(subject)

        for achievement in achievements:
            achievement: Achievement = Achievement.query.filter_by(name=achievement).first()
            teacher.achievements.append(achievement)

        for hobby in hobbies:
            hobby: Hobby = Hobby.query.filter_by(name=hobby).first()
            teacher.hobbies.append(hobby)

        image = form.image.data
        if image is not None:
            image.save(os.path.join(app.config['UPLOAD_PATH'], str(teacher.id) + '.png'))

        db.session.commit()
        return redirect(url_for('admin.index'))

    elif request.method == 'GET':
        form.name.data = teacher.name
        form.surname.data = teacher.surname
        form.tariff.data = teacher.tariff
        form.student_class.data = teacher.students_class
        form.school.data = teacher.school
        form.about_text.data = teacher.about_text
        if teacher.image:
            form.image_path = os.path.join('/static/teachers_images', teacher.image)
        form.feedback.data = teacher.feedback

        form.subjects = [i.name for i in teacher.subjects]

        form.achievements = [i.name for i in teacher.achievements]
        form.achievements_text.data = teacher.achievements_text

        form.hobbies = [i.name for i in teacher.hobbies]
        form.hobbies_text.data = teacher.hobbies_text

    return render_template('admin/edit_teacher.html', form=form, title='Edit teacher')


@bp.route('/search_form', methods=['POST'])
@login_required
def search_form():
    subjects = request.form.getlist('subjects')
    age = request.form.getlist('age')
    achievements = request.form.getlist('achievements')
    tariff = request.form.get('tariff')
    hobbies = request.form.get('hobbies')
    names = request.form.get('names')
    return redirect(url_for('admin.index', subjects=subjects, age=age, achievements=achievements, tariff=tariff,
                            hobbies=hobbies, names=names))

@bp.route('/teacher_profile/<int:id>', methods=['GET'])
def teachers_profile(id):
    teacher = db.session.get(Teacher, id)
    return render_template('admin/teacher_profile.html', teacher=teacher)
