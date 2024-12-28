from app import app
from app.models import Teacher, Achievement, Subject


@app.route('/')
@app.route('/index')
def index():
    return 'Hello'