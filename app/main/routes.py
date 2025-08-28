from random import shuffle

from flask import jsonify, redirect, render_template, request, url_for

from app import db, models
from app.main import bp
from app.main.forms import AddCommentForm
from app.models import (Achievement, Comment, Hobby, Page, ParentReply, StudyPath,
                        Subject, Teacher)
from config import config



@bp.route('/back')
def back():
    return render_template("main/a.html")


@bp.route('/')
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



#    if data.getlist('hobbies'):
#        for hobby in data.getlist('hobbies'):
#            hobby: Hobby = Hobby.query.filter_by(name=hobby).first()
#            teachers.extend(hobby.teachers)
#
#    if data.getlist('achievements'):
#        for achievement in data.getlist('achievements'):
#            achievement: Achievement = Achievement.query.filter_by(name=achievement).first()
#            teachers.extend(achievement.teachers)


#    if data.get('age'):
#        print(data.getlist('age'))
#        ages = list(map(int, data.getlist('age')))
#        print(ages)
#
#        teachers.extend(Teacher.query.filter(Teacher.students_class.in_(ages)).all())
#        print(teachers)
#
#    if data.getlist('tariff'):
#        filtered_by_tarrif = []
#        filter_params = data.getlist('tariff')
#        print(filter_params)
#        if '0' in filter_params:
#            print("Filtering by tariff <= 800")
#            filtered_by_tarrif = Teacher.query.filter(Teacher.tariff <= 800).all()
#        if '1' in filter_params:
#            filtered_by_tarrif = Teacher.query.filter(1200 > Teacher.tariff, Teacher.tariff > 800).all()
#        if '2' in filter_params:
#            filtered_by_tarrif = Teacher.query.filter(Teacher.tariff >= 1200).all()
#        print(filtered_by_tarrif)
#        teachers.extend(filtered_by_tarrif)
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
    arguments = request.args
    teachers = []
    search = False
    subject = arguments.get('subject')
    study_path = arguments.get('study_path')
    subjects = [subject]

    if subject is None and study_path is None: 
        teachers = Teacher.query.all()
        

    else:
        search = True
        if subject == 'Социальные' or subject == 'Соц-гум':
            subjects.extend(['История', 'Обществознание'])
        if subject == 'Иностранные' or subject == 'Иностранный':
            subjects.extend(['Немецкий', 'Французский'])
        if subject == 'Другие':
            subjects.extend(['Астрономия', "Право"])
        if subject == 'Хим-Био':
            subjects.extend(['Химия', 'Биология'])
        if subject.lower() == 'математика' or subject.lower == "физика":
            subjects.extend(['Физ-Мат'])
        if subject and study_path:
            pass_subjects = Subject.query.filter(Subject.name.in_(subjects)).all()
            for sub in pass_subjects:
                for teacher in sub.teachers:
                    print(teacher.study_path)
                    if teacher.study_path == StudyPath[study_path]:
                        teachers.append(teacher)
        elif subject:
            print(subjects)
            pass_subjects = Subject.query.filter(Subject.name.in_(subjects)).all()
            print(pass_subjects)
            for sub in pass_subjects:
                for teacher in sub.teachers:
                    teachers.append(teacher)
        elif study_path:
            teachers = Teacher.query.filter_by(study_path=study_path).all()
        else:
            teachers = Teacher.query.all()

    teachers = list(set(teachers))
    if teachers:
        # teachers = sorted(teachers, key=lambda x: x.position)
        shuffle(teachers)

#    all_achievements = models.Achievement.query.filter(Achievement.enabled).all()
#    if Achievement(name='другие...') in all_achievements:
#        all_achievements = list(filter(lambda x: x.name != 'другие...', all_achievements))
#        all_achievements.append(models.Achievement(name='другие...'))

    # all_hobbies = models.Hobby.query.filter(Hobby.enabled).all()
    # if Hobby(name='другие...') in all_hobbies:
    #     all_hobbies = list(filter(lambda x: x.name != 'другие...', all_hobbies))
    #     all_hobbies.append(models.Hobby(name='другие...'))
 
    replies=ParentReply.query.all()
    return render_template('main/teachers.html', teachers=teachers,
                           all_subjects=models.Subject.query.filter(Subject.enabled).all(),
                           search=search, subject=subject, subjects=subjects, all_study_paths=list(StudyPath), study_path=study_path, host=config.TEACHERS_HOST, bot_host=config.BOT_HOST, replies=replies)


@bp.route('/search_form', methods=['POST', 'GET'])
def search_form():
    subject = request.args.get('subject')
    subjects = [subject]
    study_path = request.args.get('study_path')
    if subject == 'Социальные' or subject == 'Соц-гум':
        subjects.extend(['История', 'Обществознание'])
    if subject == 'Иностранные':
        subjects.extend(['Немецкий', 'Французский'])
    if subject == 'Другие':
        subjects.extend(['Астрономия', "Право"])
    if subject == 'Химбио':
        subjects.extend(['Химия', 'Биология'])
    age = request.form.getlist('age')
    achievements = request.form.getlist('achievements')
    tariff = request.form.getlist('tariff')
    
    # hobbies = request.form.get('hobbies')
    names = request.form.get('names')
    return redirect(url_for('main.teachers', subjects=subjects, age=age, achievements=achievements, tariff=tariff,
                            names=names, search=True, study_path=study_path))


# @bp.route('/')
# def index():
#     page = Page.query.filter_by(name='index').first()
#     if not page:
#         page = Page(name='index')
#         db.session.add(page)
#         db.session.commit()
#     if not page.description:
#         page.description = 'Главная страница'
#     page.quantity += 1
#     db.session.commit()
#     return render_template('main/index.html')

@bp.route('/answer_and_questions')
def answer_and_questions():
    page = Page.query.filter_by(name='answer_and_questions').first()
    if not page:
        page = Page(name='answer_and_questions')
        db.session.add(page)
        db.session.commit()
    if not page.description:
        page.description = 'Вопросы и ответы'
    page.quantity += 1
    db.session.commit()
    return render_template('main/questions_and_answers.html', host=config.TEACHERS_HOST, bot_host=config.BOT_HOST)

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
    return render_template('main/teacher_profile.html', teacher=teacher, text=text, days=days, schedule=schedule, host=config.TEACHERS_HOST, bot_host=config.BOT_HOST)


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
    replies = ParentReply.query.all() 
    return render_template('main/about.html', replies=replies, host=config.TEACHERS_HOST, bot_host=config.BOT_HOST)


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
    return render_template('main/invite.html', host=config.TEACHERS_HOST, bot_host=config.BOT_HOST)

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
