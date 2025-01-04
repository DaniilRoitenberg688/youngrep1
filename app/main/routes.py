from app.main import bp
from app import app, data_base, end_age, achievements, subjects, hobbies
from flask import redirect, render_template, request, url_for
from app.write_log import write_log
from app.models import Teacher, Hobby, Achievement, Subject
from app import db




@bp.route('/teachers')
def teachers():
    teachers = []
    data = request.args
    search = data.get('search', False)

    if search and len(data) == 1 or not data:
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
    if teachers:
        teachers = sorted(teachers, key=lambda x: x.feedback)

    return render_template('main/teachers.html', teachers=teachers, all_subjects=subjects,
                           all_achievements=achievements, all_hobbies=hobbies, search=search)


@bp.route('/search_form', methods=['POST'])
def search_form():
    subjects = request.form.getlist('subjects')
    age = request.form.getlist('age')
    achievements = request.form.getlist('achievements')
    tariff = request.form.get('tariff')
    hobbies = request.form.get('hobbies')
    names = request.form.get('names')
    return redirect(url_for('main.teachers', subjects=subjects, age=age, achievements=achievements, tariff=tariff,
                            hobbies=hobbies, names=names, search=True))

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html')


@bp.route('/teacher_profile/<int:id>', methods=['GET'])
def teachers_profile(id):
    teacher = db.session.get(Teacher, id)
    return render_template('main/teacher_profile.html', teacher=teacher)



@bp.route('/about')
def about():
    return render_template('main/about.html')


@bp.route('/checking_system')
def checking_system():
    return render_template('main/checking_system.html')


@bp.route('/invite')
def invite():
    return render_template('main/invite.html')

@bp.route('/update_photos')
def update_photos():
    data_base.load_images()
    return redirect('/')