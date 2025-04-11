from app.main import bp
from flask import redirect, render_template, request, url_for, jsonify
from app.models import Teacher, Hobby, Achievement, Subject, Page, Comment
from app.main.forms import AddCommentForm
from app import db
from app import models


@bp.route('/teachers')
def teachers():
    page = Page.query.filter_by(name='teacher').first()
    if page is None:
        page = Page(name='teacher')
        db.session.add(page)
        db.session.commit()
    if not page.description:
        page.description = 'Страница учителей'
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

    subjects = data.getlist('subjects')
    if data.getlist('subjects'):
        for subject in data.getlist('subjects'):
            subject: Subject = Subject.query.filter_by(name=subject).first()
            teachers.extend(subject.teachers)

    if data.get('age'):
        teachers.extend(Teacher.query.filter_by(students_class=int(data.get('age'))
                                                ).all())

    if data.get('tariff'):
        filtered_by_tarrif = []
        filter_param = data.get('tariff')
        if filter_param == 0:
            filtered_by_tarrif = Teacher.query.filter(Teacher.tariff <= 800).all()
        elif filter_param == 1:
            filtered_by_tarrif = Teacher.query.filter(1200 > Teacher.tariff > 800).all()
        elif filter_param == 2:
            filtered_by_tarrif = Teacher.query.filter(Teacher.tariff >= 1200).all()
            
        teachers.extend(filtered_by_tarrif)

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
        teachers = sorted(teachers, key=lambda x: x.position)

    all_achievements = models.Achievement.query.filter(Achievement.enabled).all()
    if Achievement(name='другие...') in all_achievements:
        all_achievements = list(filter(lambda x: x.name != 'другие...', all_achievements))
        all_achievements.append(models.Achievement(name='другие...'))

    # all_hobbies = models.Hobby.query.filter(Hobby.enabled).all()
    # if Hobby(name='другие...') in all_hobbies:
    #     all_hobbies = list(filter(lambda x: x.name != 'другие...', all_hobbies))
    #     all_hobbies.append(models.Hobby(name='другие...'))

    return render_template('main/teachers.html', teachers=teachers,
                           all_subjects=models.Subject.query.filter(Subject.enabled).all(),
                           all_achievements=all_achievements, search=search, subjects=subjects)


@bp.route('/search_form', methods=['POST', 'GET'])
def search_form():
    subject = request.args.get('subject')
    subjects = [subject]
    if subject == 'Социальные' or subject == 'Соц-гум':
        subjects.extend(['История', 'Обществознание'])
    if subject == 'Иностранные':
        subjects.extend(['Немецкий', 'Французский'])
    if subject == 'Другие':
        subjects.extend(['Астрономия'])
    if subject == 'Химбио':
        subjects.extend(['Химия', 'Биология'])
    age = request.form.getlist('age')
    achievements = request.form.getlist('achievements')
    tariff = request.form.get('tariff')
    # hobbies = request.form.get('hobbies')
    names = request.form.get('names')
    return redirect(url_for('main.teachers', subjects=subjects, age=age, achievements=achievements, tariff=tariff,
                            names=names, search=True))


@bp.route('/')
def index():
    page = Page.query.filter_by(name='index').first()
    if not page:
        page = Page(name='index')
        db.session.add(page)
        db.session.commit()
    if not page.description:
        page.description = 'Главная страница'
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
    if not page.description:
        page.description = 'Профили учителей'
    page.quantity += 1
    db.session.commit()
    teacher = db.session.get(Teacher, id)
    if teacher.shown_times is None:
        teacher.shown_times = 0
    teacher.shown_times += 1
    db.session.commit()
    with open('app/static/free_text/free_text.txt', 'r') as file:
        text = file.read()
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    schedule = teacher.parse_schedule()
    return render_template('main/teacher_profile.html', teacher=teacher, text=text, days=days, schedule=schedule)


@bp.route('/about')
def about():
    page = Page.query.filter_by(name='about').first()
    if not page:
        page = Page(name='about')
        db.session.add(page)
        db.session.commit()
    if not page.description:
        page.description = 'О нас'
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
    if not page.description:
        page.description = 'Checking система'
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
    if not page.description:
        page.description = 'Работа у нас'
    page.quantity += 1
    db.session.commit()
    return render_template('main/invite.html')

@bp.route('/add_statistic/<name>', methods=['POST'])
def add_statistic(name):
    names = {'pop_up_bot': 'нажатие попапа с ботом',
             'pop_up_manager': 'нажатие попапа с менеджером',
             'bot_popup': 'переход в бота с попапа',
             'manager': 'переход в менеджера',
             'bot_checking_system': 'переход на бота чекинг системы',
             'chanel': 'переход в канал',
             'manager_invite': 'переход в менеджера с "работать у нас"',
             'bot': 'переход в бота с кнопок'}

    if name in names:
        page: Page = Page.query.filter_by(name=name).first()
        if page:
            if not page.description:
                page.description = names.get(name)

            page.quantity += 1

        else:
            page = Page(name=name, description=names.get(name), quantity=1)
            db.session.add(page)

        db.session.commit()
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'not found'}), 404


@bp.route('/add_comment/<teacher_id>', methods=['POST', 'GET'])
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
        return redirect(url_for('main.teachers_profile', id=teacher.id))

    return render_template('main/add_comment.html', form=form, teacher=teacher)
