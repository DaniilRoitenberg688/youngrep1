from unicodedata import category
from urllib.parse import urlsplit
import os

from app import db
from app.admin import bp
from flask import render_template, redirect, session, url_for, flash, request, current_app, jsonify, send_file
from app.admin.forms import LoginForm, AddTeacherForm, EditTeacherForm, EditSearchForm, AddSearchForm, EditFreeText, \
    AddCommentForm, EditCommentForm, EditSearchParamForm, ReplyForm
from flask_login import current_user, login_user, login_required, logout_user

from app.models import StudyPath, User, Teacher, Subject, Achievement, Hobby, Page, Comment, ParentReply

from app import models
from secrets import token_urlsafe


@bp.route('/back')
def back():
    return send_file("templates/admin/a.html")

@bp.route('/')
@login_required
def index():
    if current_user.teacher:
        return render_template('admin/index.html', title='Teachers', teachers=[current_user.teacher])
    teachers = []
    data = request.args
    print(data.getlist('subjects'))
    if not data:
        teachers = Teacher.query.all()

#    if data.getlist('hobbies'):
#        for hobby in data.getlist('hobbies'):
#            hobby: Hobby = Hobby.query.filter_by(name=hobby).first()
#            teachers.extend(hobby.teachers)
#
#    if data.getlist('achievements'):
#        for achievement in data.getlist('achievements'):
#            achievement: Achievement = Achievement.query.filter_by(name=achievement).first()
#            teachers.extend(achievement.teachers)

    if data.getlist('subjects'):
        for subject in data.getlist('subjects'):
            subject: Subject = Subject.query.filter_by(name=subject).first()
            teachers.extend(subject.teachers)

#    if data.get('age'):
#        teachers.extend(Teacher.query.filter_by(students_class=int(data.get('age'))
#                                                ).all())
#
#    if data.get('tariff'):
#        teachers.extend(Teacher.query.filter(Teacher.tariff <= int(data.get('tariff'))).all())
#
#    if data.get('names'):
#        names = data.get('names').split()
#        result = []
#        if len(names) == 1:
#            result = Teacher.query.filter(
#                names[0] == Teacher.surname
#            ).all()
#
#            if not result:
#                result = Teacher.query.filter(
#                    names[0] == Teacher.name
#                ).all()
#        if len(names) == 2:
#            result = Teacher.query.filter(
#                names[0] == Teacher.surname or names[1] == Teacher.name
#            ).all()
#            if not result:
#                result = Teacher.query.filter(
#                    names[1] == Teacher.surname or names[0] == Teacher.name
#                ).all()
#
#        teachers.extend(result)
    
    if data.get('study_path', 0):
        print(data.get('study_path'))
        teachers.extend(Teacher.query.filter_by(study_path=data.get('study_path'))) 
        

    teachers = list(set(teachers))
    teachers = sorted(teachers, key=lambda x: x.position)

    return render_template('admin/index.html', title='Teachers', teachers=teachers,
                           all_subjects=models.Subject.query.filter(Subject.enabled).all(),
                           all_achievements=models.Achievement.query.filter(Achievement.enabled).all(),
                           all_hobbies=models.Hobby.query.filter(Hobby.enabled).all())


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

@bp.route('/add_reply', methods=['POST', "GET"])
@login_required
def add_reply():
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    form = ReplyForm()
    if form.validate_on_submit():
        new_reply = ParentReply()
        new_reply.parent_name = form.parent_name.data
        new_reply.reply_text = form.reply_text.data
        new_reply.bottom_text = form.bottom_text.data
        db.session.add(new_reply)
        db.session.commit()
        return redirect(url_for('admin.replies'))

    return render_template('admin/reply_form.html', form=form, title='Add teacher')

@bp.route('/edit_reply/<id>', methods=['POST', "GET"])
@login_required
def edit_reply(id):
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    form = ReplyForm()
    reply: ParentReply = db.session.get(ParentReply, id)
    if form.validate_on_submit():
        reply.parent_name = form.parent_name.data
        reply.reply_text = form.reply_text.data
        reply.bottom_text = form.bottom_text.data
        db.session.commit()
        return redirect(url_for('admin.replies'))

    elif request.method == 'GET':
        form.parent_name.data = reply.parent_name
        form.bottom_text.data = reply.bottom_text
        form.reply_text.data = reply.reply_text


    return render_template('admin/reply_form.html', form=form, title='Add teacher')

@bp.route('/delete_reply/<id>')
def delete_reply(id):
    reply = db.session.get(ParentReply, id)
    db.session.delete(reply)
    db.session.commit()
    return redirect(url_for('admin.replies'))

@bp.route('/reply')
@login_required
def replies():
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    all_replies = ParentReply.query.all()
    return render_template('admin/all_replies.html', replies=all_replies, title='All replies')


@bp.route('/teacher', methods=['GET', 'POST'])
@login_required
def new_teacher():
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    form = AddTeacherForm()
    form.all_achievements = Achievement.query.all()
    form.all_hobbies = Hobby.query.all()
    form.all_subjects = Subject.query.all()
    if form.validate_on_submit():

        teacher = Teacher(
            name=form.name.data,
            surname=form.surname.data,
            students_class=form.student_class.data,
            school=form.school.data,
            about_text=form.about_text.data,
            tariff=form.tariff.data,
            achievements_text=form.achievements_text.data,
            hobbies_text=form.hobbies_text.data,
            is_free=int(request.form.get('is_free', 0)),
        )

        db.session.add(teacher)
        db.session.commit()

        hobbies_to_add = request.form.getlist('hobbies')
        if not hobbies_to_add:
            empty_hobby = Hobby.query.filter(Hobby.name == '').first()
            print(empty_hobby)
            teacher.hobbies.append(empty_hobby)
        else:
            for i in hobbies_to_add:
                hobby = Hobby.query.filter(Hobby.name == i).first()
                hobby.teachers
                teacher.hobbies.append(hobby)

        subjects_to_add = request.form.getlist('subjects')
        if not subjects_to_add:
            empty = Subject.query.filter(Subject.name == '').first()
            print(empty)
            teacher.subjects.append(empty)
            teacher.is_shown = False
        else:
            for i in subjects_to_add:
                subject = Subject.query.filter(Subject.name == i).first()
                subject.teachers
                teacher.subjects.append(subject)

        achievements_to_add = request.form.getlist('achievements')
        if not achievements_to_add:
            empty = Achievement.query.filter(Achievement.name == '').first()
            print(empty)
            teacher.achievements.append(empty)
        else:
            for i in achievements_to_add:
                achievement = Achievement.query.filter(Achievement.name == i).first()
                achievement.teachers
                teacher.achievements.append(achievement)

        study_path = request.form.get('study_paths', '')
        teacher.study_path = StudyPath[study_path.split('.')[1]] 

        db.session.commit()

        image = form.image.data
        if image is not None:
            image.save(os.path.join(current_app.config['UPLOAD_PATH'], str(teacher.id) + '.png'))
            teacher.image = str(teacher.id) + '.png'
            db.session.commit()

        teacher.position = teacher.id

        user = User()
        user.login = f'teacher_{teacher.id}'
        user.teacher = teacher
        user.set_password(token_urlsafe(8))
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('admin.index'))

    return render_template('admin/add_teacher.html', form=form, title='Add teacher')


@bp.route('/delete_teacher/<int:id>', methods=['GET', 'DELETE'])
@login_required
def delete_teacher(id):
    teacher = db.session.get(Teacher, id)
    if teacher.image:
        os.remove(os.path.join(current_app.config['UPLOAD_PATH'], teacher.image))
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for('admin.index'))


@bp.route('/edit_teacher/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
    form = EditTeacherForm()
    form.all_achievements = Achievement.query.all()
    form.all_hobbies = Hobby.query.all()
    form.all_subjects = Subject.query.all()
    teacher: Teacher = db.session.get(Teacher, id)
    if form.validate_on_submit():
        teacher.name = form.name.data
        teacher.surname = form.surname.data
        teacher.tariff = form.tariff.data
        teacher.students_class = form.student_class.data
        teacher.school = form.school.data
        teacher.about_text = form.about_text.data
        # teacher.feedback = form.feedback.data
        teacher.achievements_text = form.achievements_text.data
        teacher.hobbies_text = form.hobbies_text.data

        if not current_user.teacher:
            teacher.is_free = int(request.form.get('is_free', 0))

        study_path = request.form.get('study_paths', '')
        teacher.study_path = StudyPath[study_path.split('.')[1]] 

        teacher.subjects.clear()
        teacher.hobbies.clear()
        teacher.achievements.clear()

        hobbies_to_add = request.form.getlist('hobbies')
        if not hobbies_to_add:
            empty_hobby = Hobby.query.filter(Hobby.name == '').first()
            print(empty_hobby)
            teacher.hobbies.append(empty_hobby)
        else:
            for i in hobbies_to_add:
                hobby = Hobby.query.filter(Hobby.name == i).first()
                hobby.teachers
                teacher.hobbies.append(hobby)

        subjects_to_add = request.form.getlist('subjects')
        if not subjects_to_add:
            empty = Subject.query.filter(Subject.name == '').first()
            print(empty)
            teacher.subjects.append(empty)
            teacher.is_shown = False
        else:
            for i in subjects_to_add:
                subject = Subject.query.filter(Subject.name == i).first()
                subject.teachers
                teacher.subjects.append(subject)

        achievements_to_add = request.form.getlist('achievements')
        if not achievements_to_add:
            empty = Achievement.query.filter(Achievement.name == '').first()
            print(empty)
            teacher.achievements.append(empty)
        else:
            for i in achievements_to_add:
                achievement = Achievement.query.filter(Achievement.name == i).first()
                achievement.teachers
                teacher.achievements.append(achievement)

        image = form.image.data
        if image is not None:
            image.save(os.path.join(current_app.config['UPLOAD_PATH'], str(teacher.id) + '.png'))
            teacher.image = str(teacher.id) + '.png'
            db.session.commit()

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

        form.is_free = teacher.is_free

        form.study_path = teacher.study_path

    return render_template('admin/edit_teacher.html', form=form, title='Edit teacher')


@bp.route('/search_form', methods=['POST'])
@login_required
def search_form():
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    subjects = request.form.getlist('subjects')
    age = request.form.getlist('age')
    achievements = request.form.getlist('achievements')
    tariff = request.form.get('tariff')
    hobbies = request.form.get('hobbies')
    names = request.form.get('names')
    return redirect(url_for('admin.index', subjects=subjects, age=age, achievements=achievements, tariff=tariff,
                            hobbies=hobbies, names=names))


@bp.route('/teacher_profile/<int:id>', methods=['GET'])
@login_required
def teachers_profile(id):
    teacher = db.session.get(Teacher, id)
    if current_user.teacher:
        if current_user.teacher != teacher:
            return redirect(url_for('admin.index'))
    with open('app/static/free_text/free_text.txt', 'r') as file:
        text = file.read()
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    schedule = teacher.parse_schedule()
    page: Page = Page.query.filter_by(name='teacher_profile').first()
    percent = int(round(teacher.shown_times / page.quantity, 2) * 100)
    return render_template('admin/teacher_profile.html', teacher=teacher, text=text, days=days, schedule=schedule,
                           percent=percent)


@bp.route('/edit_search', methods=['GET', 'POST'])
@login_required
def edit_search():
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    form = EditSearchForm()
    form.subjects = Subject.query.all()
    form.achievements = Achievement.query.all()
    form.hobbies = Hobby.query.all()
    if form.validate_on_submit():
        print('sadad')
        print(request.form.getlist('subjects'))
        for i in form.subjects:
            if i.name in request.form.getlist('subjects'):
                i.enabled = True
            else:
                i.enabled = False
        for i in form.achievements:
            if i.name in request.form.getlist('achievements'):
                i.enabled = True
            else:
                i.enabled = False
        for i in form.hobbies:
            if i.name in request.form.getlist('hobbies'):
                i.enabled = True
            else:
                i.enabled = False
        db.session.commit()

        # return redirect(url_for('admin.index'))

    return render_template('admin/edit_search.html', title='Edit search data', form=form)


@bp.route('/add_search', methods=['GET', 'POST'])
@login_required
def add_search():
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    form = AddSearchForm()
    if form.validate_on_submit():
        category = form.category.data
        if category == 'Предмет':
            if Subject.query.filter_by(name=form.name.data).first():
                flash('Not uniq name')
                return redirect(url_for('admin.add_search'))
            else:
                n = Subject(name=form.name.data)
                db.session.add(n)
                db.session.commit()
                return redirect(url_for('admin.edit_search'))

        if category == 'Достижение':
            if Achievement.query.filter_by(name=form.name.data).first():
                flash('Not uniq name')
                return redirect(url_for('admin.add_search'))
            else:
                n = Achievement(name=form.name.data)
                db.session.add(n)
                db.session.commit()
                return redirect(url_for('admin.edit_search'))

        if category == 'Хобби':
            if Hobby.query.filter_by(name=form.name.data).first():
                flash('Not uniq name')
                return redirect(url_for('admin.add_search'))
            else:
                n = Hobby(name=form.name.data)
                db.session.add(n)
                db.session.commit()
                return redirect(url_for('admin.edit_search'))
    return render_template('admin/add_search.html', title='Add something', form=form)


@bp.route('/edit_search_param/<type>/<id>', methods=['GET', 'POST'])
@login_required
def edit_search_param(type, id):
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    form = EditSearchParamForm()
    categories = {'subject': Subject, 'achievement': Achievement, 'hobby': Hobby}
    to_edit: Subject | Achievement | Hobby = db.session.get(categories.get(type), id)

    if request.method == 'GET':
        form.name.data = to_edit.name
        return render_template('admin/edit_search_param.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            to_edit.name = form.name.data
            db.session.commit()
            return redirect(url_for('admin.edit_search'))
        return render_template('admin/edit_search_param.html', form=form)


@bp.route('/statistic')
@login_required
def statistic():
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    pages: list[Page] = Page.query.all()
    page: Page = Page.query.filter_by(name='teacher_profile').first()

    pages = [{'description': i.description.capitalize(), 'quantity': i.quantity} for i in pages]
    teachers = Teacher.query.all()
    teachers = [
        {'name': i.name, 'surname': i.surname, 'shown_times': i.shown_times,
         'percent': int(round(i.shown_times / page.quantity, 2) * 100)}
        for i in teachers]
    return render_template('admin/statistic.html', title='statistic', pages=pages, teachers=teachers,
                           sum_teachers=page.quantity)


@bp.route('/free_text')
@login_required
def free_text():
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    with open('app/static/free_text/free_text.txt', 'r') as file:
        text = file.read()
    return render_template('admin/free_text.html', text=text)


@bp.route('/edit_free_text', methods=['POST', 'GET'])
def edit_free_text():
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    form = EditFreeText()
    if request.method == 'GET':
        with open('app/static/free_text/free_text.txt', 'r') as file:
            text = file.read()
        form.text.data = text
        return render_template('admin/edit_free_text.html', form=form, title='Edit free text')

    if form.validate_on_submit():
        with open('app/static/free_text/free_text.txt', 'w') as file:
            file.write(form.text.data)

        return redirect(url_for('admin.free_text'))


@bp.route('/edit_schedule/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_schedule(id):
    teacher = db.session.get(Teacher, id)
    if request.method == 'GET':
        days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        print(teacher.schedule)
        schedule = teacher.parse_schedule()
        print(schedule)
        return render_template('admin/edit_schedule.html', days=days, schedule=schedule)

    if request.method == 'POST':
        data = request.form.getlist('time')
        result = {}
        for i in data:
            day, time = i.split(':')
            if day not in result:
                result[day] = [time]
            else:
                result[day].append(time)
        print(result)
        teacher.set_schedule(result)
        db.session.commit()
        return redirect(url_for('admin.edit_schedule', id=id))


@bp.route('/change_visibility/<int:id>', methods=['POST'])
def change_visibility(id):
    teacher = db.session.get(Teacher, id)
#    if teacher.subjects[0].name == '' or teacher.achievements[0].name == '' or teacher.hobbies[0].name == '':
#        return jsonify({'id': id, 'changed': False})
    teacher.is_shown = not teacher.is_shown
    if teacher.is_shown is None:
        teacher.is_shown = True
    print(teacher.is_shown)
    db.session.commit()
    return jsonify({'id': id, 'changed': True})


@bp.route('/add_comment/<teacher_id>', methods=['POST', 'GET'])
@login_required
def add_comment(teacher_id):
    teacher = db.session.get(Teacher, teacher_id)
    if not teacher:
        return redirect(url_for('admin.index'))

    form = AddCommentForm()
    if form.validate_on_submit():
        comment = Comment()
        comment.user_name = form.user_name.data
        comment.text = form.comment.data
        comment.feedback = form.feedback.data
        comment.teacher = teacher
        db.session.add(comment)
        db.session.commit()
        teacher.feedback = round(sum(map(lambda x: x.feedback, teacher.comments)) / len(teacher.comments))
        db.session.commit()
        return redirect(url_for('admin.teachers_profile', id=teacher.id))

    return render_template('admin/add_comment.html', form=form, teacher=teacher)


@bp.route('/delete_comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    teacher: Teacher = comment.teacher

    db.session.delete(comment)
    db.session.commit()

    if teacher.comments:
        teacher.feedback = round(sum(map(lambda x: x.feedback, teacher.comments)) / len(teacher.comments))
    else:
        teacher.feedback = 0
    db.session.commit()
    return redirect(url_for('admin.teachers_profile', id=teacher.id))


@bp.route('/edit_comment/<comment_id>', methods=['GET', 'POST'])
def edit_comment(comment_id):
    form = EditCommentForm()
    comment = db.session.get(Comment, comment_id)
    teacher = comment.teacher
    if request.method == 'GET':
        form.user_name.data = comment.user_name
        form.comment.data = comment.text
        form.feedback.data = comment.feedback
        return render_template('admin/edit_comment.html', form=form, teacher=teacher)

    if request.method == 'POST':
        if form.validate_on_submit():
            comment.user_name = form.user_name.data
            comment.feedback = form.feedback.data
            comment.text = form.comment.data
            db.session.commit()
            teacher.feedback = round(sum(map(lambda x: x.feedback, teacher.comments)) / len(teacher.comments))
            db.session.commit()
            return redirect(url_for('admin.teachers_profile', id=teacher.id))


@bp.route('/oder')
@login_required
def oder():
    if current_user.teacher:
        return redirect(url_for('admin.index'))
    return send_file('templates/admin/oder.html')


@bp.route('/api/teachers')
def api_teachers():
    teachers = Teacher.query.filter_by(is_shown=True).all()
    teachers = sorted(teachers, key=lambda x: x.position)
    print(teachers)
    return jsonify([i.as_dict() for i in teachers]), 200


@bp.route('/api/teachers', methods=['PATCH'])
def patch_teachers():
    data = request.json
    print(data)
    teacher_0_data = data[0]
    teacher_1_data = data[1]
    teacher_0 = db.session.get(Teacher, int(teacher_0_data.get('id')))
    teacher_0.position = teacher_0_data.get('position')

    teacher_1 = db.session.get(Teacher, int(teacher_1_data.get('id')))
    teacher_1.position = teacher_1_data.get('position')
    db.session.commit()
    teachers = Teacher.query.filter_by(is_shown=True).all()
    teachers = sorted(teachers, key=lambda x: x.position)
    print(teachers)
    return jsonify([i.as_dict() for i in teachers]), 200


@bp.route('/api/teacher/<id>', methods=['PATCH'])
def make_first(id):
    teacher: Teacher = db.session.get(Teacher, id)
    all_teachers: list[Teacher] = sorted(Teacher.query.filter_by(is_shown=True).all(), key=lambda x: x.position)
    first = all_teachers[0].position
    print(all_teachers)
    index_before = all_teachers.index(teacher)
    for i in range(index_before + 1):
        if i == index_before:
            all_teachers[i].position = first
        else:
            all_teachers[i].position = all_teachers[i + 1].position
        print(i)
    db.session.commit()
    print(sorted(Teacher.query.filter_by(is_shown=True).all(), key=lambda x: x.position))
    return jsonify([i.as_dict() for i in sorted(Teacher.query.filter_by(is_shown=True).all(), key=lambda x: x.position)]), 200

