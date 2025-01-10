from app.main import bp
from flask import redirect, render_template, request, url_for
from app.models import Teacher, Hobby, Achievement, Subject, Page
from app import db
from app import models


@bp.route('/teachers')
def teachers():
    page = Page.query.filter_by(name='teacher').first()
    if page is None:
        page = Page(name='teacher')
        db.session.add(page)
        db.session.commit()
    if not request.args.get('search'):
        print(page.name)
        page.quantity += 1
        db.session.commit()
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
        teachers = sorted(teachers, key=lambda x: -x.feedback)


    all_achievements = models.Achievement.query.filter(Achievement.enabled).all()
    if Achievement(name='другие...') in all_achievements:
        all_achievements = list(filter(lambda x: x.name != 'другие...', all_achievements))
        all_achievements.append(models.Achievement(name='другие...'))

    all_hobbies = models.Hobby.query.filter(Hobby.enabled).all()
    if Hobby(name='другие...') in all_hobbies:
        all_hobbies = list(filter(lambda x: x.name != 'другие...', all_hobbies))
        all_hobbies.append(models.Hobby(name='другие...'))

    return render_template('main/teachers.html', teachers=teachers, all_subjects=models.Subject.query.filter(Subject.enabled).all(),
                           all_achievements=all_achievements, all_hobbies=all_hobbies, search=search)


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
    page = Page.query.filter_by(name='index').first()
    if not page:
        page = Page(name='index')
        db.session.add(page)
        db.session.commit()
    page.quantity += 1
    db.session.commit()
    return render_template('main/index.html')


@bp.route('/teacher_profile/<int:id>', methods=['GET'])
def teachers_profile(id):
    page = Page.query.filter_by(name='teacher_profile').first()
    if not page:
        page = Page(name='teacher_profile')
        db.session.add(page)
        db.session.commit()
    page.quantity += 1
    db.session.commit()
    teacher = db.session.get(Teacher, id)
    return render_template('main/teacher_profile.html', teacher=teacher)



@bp.route('/about')
def about():
    page = Page.query.filter_by(name='about').first()
    if not page:
        page = Page(name='about')
        db.session.add(page)
        db.session.commit()
    page.quantity += 1
    db.session.commit()
    return render_template('main/about.html')


@bp.route('/checking_system')
def checking_system():
    page = Page.query.filter_by(name='checking_system').first()
    if not page:
        page = Page(name='checking_system')
        db.session.add(page)
        db.session.commit()
    page.quantity += 1
    db.session.commit()
    return render_template('main/checking_system.html')


@bp.route('/invite')
def invite():
    page = Page.query.filter_by(name='invite').first()
    if not page:
        page = Page(name='invite')
        db.session.add(page)
        db.session.commit()
    page.quantity += 1
    db.session.commit()
    return render_template('main/invite.html')
