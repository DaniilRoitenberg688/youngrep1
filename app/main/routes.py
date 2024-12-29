from app.main import bp
from app import app, data_base, end_age
from flask import redirect, render_template, request, url_for
from app.write_log import write_log
from app.models import Subject, Teacher, Achievement, Hobby

with (((app.app_context()))):
    all_achievements = [i.name for i in Achievement.query.all()]
    all_achievements.append('другие...')
    all_subjects = [i.name for i in Subject.query.all()]
    all_subjects.append('другие...')
    all_hobbies = [i.name for i in Hobby.query.all()]
    all_hobbies.append('другие...')

def parameters_to_dict(line):
    params = line.split('&')
    result = {}
    for i in params:
        param, value = i.split('=')
        result[param] = value

    return result


@bp.route('/teachers')
def teachers():
    teachers = sorted(data_base.all_teachers(), key=lambda x: -int(x[8]))
    return render_template('main/teachers.html', teachers=teachers, all_subjects=all_subjects, max_age=end_age,
                           all_achievements=all_achievements, hobbies=all_hobbies)


@bp.route('/search/<search_parameters>')
def search(search_parameters):
    try:
        parameters = parameters_to_dict(search_parameters)
        all_teachers = data_base.all_teachers()

        if not parameters.get('subject', '') and not int(parameters.get('age', 0)) and not parameters.get('achieve',
                                                                                                          '') and not parameters.get(
            'param', '') and not parameters.get('tariff', '') and not parameters.get('hobby', ''):
            return render_template('main/teachers.html', teachers=teachers, all_subjects=all_subjects, max_age=end_age,
                                   all_achievements=all_achievements, hobbies=all_hobbies, search=1)

        if parameters.get('subject', ''):
            if parameters.get('subject') == 'другие...':
                all_teachers = data_base.search_by_other_subject(teachers=all_teachers, subjects=all_subjects)
            else:
                all_teachers = data_base.search_by_subject(parameters['subject'], all_teachers)

        if int(parameters.get('age', 0)):
            all_teachers = data_base.search_by_age(int(parameters['age']), all_teachers)

        if int(parameters.get('tariff', 0)):
            all_teachers = data_base.search_by_tariff(int(parameters['tariff']), all_teachers)

        if parameters.get('achieve', ''):
            if parameters.get('achieve') == 'другие...':
                all_teachers = data_base.search_by_other_achievements(teachers=all_teachers, achievements=all_achievements)
            else:
                all_teachers = data_base.search_by_achievements(parameters['achieve'].split(','), all_teachers)

        if parameters.get('hobby', ''):
            if parameters.get('hobby') == 'другие...':
                all_teachers = data_base.search_by_other_hobbies(teachers=all_teachers, hobbies=all_hobbies)
            else:
                all_teachers = data_base.search_by_hobbies(parameters['hobby'].split(','), all_teachers)

        if parameters.get('param', ''):
            a = parameters.get('param').split()
            if len(a) == 2:
                first = a[0]
                second = a[1]
                test1 = data_base.search_by_name(first, all_teachers)
                test2 = data_base.search_by_surname(second, all_teachers)

                if test1 or test2:
                    if test1:
                        all_teachers = test1
                    if test2:
                        all_teachers = test2

                else:
                    first, second = first, second
                    test1 = data_base.search_by_name(first, all_teachers)
                    test2 = data_base.search_by_surname(second, all_teachers)

                    if test1 or test2:
                        if test1:
                            all_teachers = test1
                        if test2:
                            all_teachers = test2

            elif len(a) == 1:
                first = a[0]
                all_teachers = data_base.search_by_name(first, all_teachers)

        return render_template('main/teachers.html', teachers=all_teachers, all_subjects=all_subjects, max_age=end_age,
                               all_achievements=all_achievements, hobbies=all_hobbies, search=True)

    except Exception as e:
        write_log(e)


@bp.route('/search_form', methods=['post', 'get'])
def search_form():
    data = request.form
    subject = data.get('subject', '')
    age = data.get('age', 0)
    hobbies_ = []
    for i in data:
        if 'hobby' in i:
            hobbies_.append(data[i])

    achievements = []
    for i in data:
        if 'achieve' in i:
            achievements.append(data[i])

    return redirect(url_for('search', search_parameters=f'subject={subject}&achieve={",".join(achievements)}&age={age}&param={data.get("param")}&tariff={data.get("tariff", 0)}&hobby={",".join(hobbies_)}'))


@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/teacher_profile/<int:id>')
def teacher_profile(id):
    teacher = data_base.teacher_by_id(id)
    print(teacher[10])
    replies = teacher[10].split('; ')
    print(replies)
    return render_template('main/teachers_profile.html', teacher=teacher, replies=replies)



@bp.route('/about')
def about():
    return render_template('main/about.html')


@bp.route('/checking_system')
def checking_system():
    return render_template('main/checking_system.html')


@bp.route('/subjects')
def subjects():
    return render_template('main/subjects.html')


@bp.route('/invite')
def invite():
    return render_template('main/invite.html')

@bp.route('/update_photos')
def update_photos():
    data_base.load_images()
    return redirect('/')