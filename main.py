from doctest import debug

from flask import Flask, render_template, request
from werkzeug.utils import redirect

from execel_connector import ExcelConnector

app = Flask(__name__)

data_base = ExcelConnector()

all_subjects = ["Математика", "Информатика", "Физика", "Химия", "Биология"]
end_age = 17
all_achievements = ["победитель_ВСОШ", "призер_ВСОШ", "победитель_перечневой олимпиады_1_уровня",
                    "призер перечневой_олимпиады_1_уровня "]


def parameters_to_dict(line):
    params = line.split('&')
    result = {}
    for i in params:
        param, value = i.split('=')
        result[param] = value

    return result


@app.route('/teachers')
def teachers():
    teachers = sorted(data_base.all_teachers(), key=lambda x: -int(x[8]))
    return render_template('teachers.html', teachers=teachers, all_subjects=all_subjects, max_age=end_age,
                           all_achievements=all_achievements)


# @app.route('/search/<search_parameters>')
# def search(search_parameters):
#     parameters = parameters_to_dict(search_parameters)
#     if not parameters['subject'] and not parameters.get('param', ''):
#         return redirect('/')
#     all_teachers = data_base.all_teachers()
#     if parameters['subject']:
#         all_teachers = data_base.search_by_subject(parameters['subject'], all_teachers)
#
#     param: str = parameters.get('param', '')
#     if param:
#         if param.isdigit():
#             if int(param) > 11:
#                 all_teachers = data_base.search_by_tariff(int(param), all_teachers)
#                 return render_template('teachers.html', teachers=all_teachers, current_subject=parameters['subject'])
#
#             all_teachers = data_base.search_by_class(int(param), all_teachers)
#             return render_template('teachers.html', teachers=all_teachers, current_subject=parameters['subject'])

@app.route('/search/<search_parameters>')
def search(search_parameters):
    parameters = parameters_to_dict(search_parameters)
    all_teachers = data_base.all_teachers()

    if not parameters.get('subject', '') and not int(parameters.get('age', 0)) and not parameters.get('achieve',
                                                                                                      '') and not parameters.get(
            'param', ''):
        return redirect('/teachers')

    if parameters.get('subject', ''):
        all_teachers = data_base.search_by_subject(parameters['subject'], all_teachers)

    if int(parameters.get('age', 0)):
        all_teachers = data_base.search_by_age(int(parameters['age']), all_teachers)

    if parameters.get('achieve', ''):
        all_teachers = data_base.search_by_achievements(parameters['achieve'], all_teachers)

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


    return render_template('teachers.html', teachers=all_teachers, all_subjects=all_subjects, max_age=end_age,
                           all_achievements=all_achievements)


@app.route('/search_form/', methods=['post'])
def search_form():
    data = request.form
    subject = data.get('subject', '')
    achievement = data.get('achieve', '')
    age = data.get('age', 0)

    return redirect(f'/search/subject={subject}&achieve={achievement}&age={age}&param={data.get("param")}')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/teacher_profile/<int:id>')
def teacher_profile(id):
    teacher = data_base.teacher_by_id(id)
    replies = teacher[-1].split('; ')
    return render_template('teachers_profile.html', teacher=teacher, replies=replies)


@app.route('/materials')
def materials():
    return render_template('error.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/checking_system')
def checking_system():
    return render_template('checking_system.html')


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/subjects')
def subjects():
    return render_template('subjects.html')


@app.route('/invite')
def invite():
    return render_template('invite.html')


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
