from urllib.parse import urlsplit

from app.admin import bp
from flask import render_template, redirect, url_for, flash, request
from app.admin.forms import LoginForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User


@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html', title='Teachers')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print('sdf')
        user: User = User.query.filter_by(login=form.login.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Wrong password or username')
            return redirect(url_for('admin.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # if not next_page or urlsplit(next_page).netloc != '':
        #     next_page = url_for('admin.index')
        # return redirect(next_page)
        return redirect(url_for('admin.index'))
    print('sdfsdf')
    return render_template('admin/login.html', form=form, title='Login')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.index'))
