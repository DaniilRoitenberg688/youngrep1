from urllib.parse import urlsplit
import os

from app import app
from app.admin import bp
from flask import render_template, redirect, url_for, flash, request
from app.admin.forms import LoginForm, AddTeacherForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Teacher


@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html', title='Teachers')

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
def new_teacher():
    form = AddTeacherForm()
    if form.validate_on_submit():

        teacher = Teacher(
            name=form.name.data,
            surname=form.surname.data,
            students_class=form.student_class.data,
            school=form.school.data,
            about_text=form.about_text.data
        )

        image = form.image.data
        if image is not None:
            image.save(os.path.join(app.config['UPLOAD_PATH'], str(teacher.id) + '.png'))
            teacher.image = str(teacher.id) + '.png'




        return redirect(url_for('admin.index'))


    return render_template('admin/add_teacher.html', form=form)