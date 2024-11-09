from doctest import debug

from flask import Flask, render_template, request
from werkzeug.utils import redirect

from execel_connector import ExcelConnector

app = Flask(__name__)

data_base = ExcelConnector()


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
    return render_template('teachers.html', teachers=teachers)


@app.route('/search/<search_parameters>')
def search(search_parameters):
    parameters = parameters_to_dict(search_parameters)
    if not parameters['subject'] and not parameters.get('param', ''):
        return redirect('/')
    all_teachers = data_base.all_teachers()
    if parameters['subject']:
        all_teachers = data_base.search_by_subject(parameters['subject'], all_teachers)

    param: str = parameters.get('param', '')
    if param:
        if param.isdigit():
            if int(param) > 11:
                all_teachers = data_base.search_by_tariff(int(param), all_teachers)
                return render_template('teachers.html', teachers=all_teachers, current_subject=parameters['subject'])

            all_teachers = data_base.search_by_class(int(param), all_teachers)
            return render_template('teachers.html', teachers=all_teachers, current_subject=parameters['subject'])


        try_by_name = data_base.search_by_name(param, all_teachers)
        try_by_surname = data_base.search_by_surname(param, all_teachers)
        try_by_place = data_base.search_by_place(param, all_teachers)
        try_by_achievement = data_base.search_by_achievements(param, all_teachers)

        if try_by_name:
            return render_template('teachers.html', teachers=try_by_name, current_subject=parameters['subject'])

        if try_by_surname:
            return render_template('teachers.html', teachers=try_by_surname, current_subject=parameters['subject'])

        if try_by_place:
            return render_template('teachers.html', teachers=try_by_place, current_subject=parameters['subject'])

        if try_by_achievement:
            return render_template('teachers.html', teachers=try_by_achievement, current_subject=parameters['subject'])


    print(all_teachers)
    return render_template('teachers.html', teachers=all_teachers, current_subject=parameters['subject'])




@app.route('/search_form/<search_parameters>', methods=['post'])
def search_form(search_parameters):
    param = request.form.get('param', '')
    print(param)
    return redirect(f'/search/{search_parameters}&param={param}')




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

    app.run('0.0.0.0')
